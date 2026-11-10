#!/usr/bin/env python3
"""Ferramenta determinística para diagnósticos e simulados de certificação.
Uso (a partir da pasta da skill):
    python scripts/avaliar.py --allocate
    python scripts/avaliar.py --input caminho/para/respostas.json
Não transforma acertos em nota oficial escalonada nem prevê aprovação.
"""
import argparse
import json
import math
import sys
from pathlib import Path


class InvalidInput(ValueError):
    pass


def load_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def validate_domains(domains):
    if not isinstance(domains, list) or not domains:
        raise InvalidInput("Os domínios devem ser uma lista não vazia.")
    seen = set()
    weights = []
    for d in domains:
        if not isinstance(d, dict):
            raise InvalidInput("Cada domínio deve ser um objeto.")
        code = d.get("id")
        if not isinstance(code, str) or not code.strip() or code in seen:
            raise InvalidInput("IDs de domínio devem ser textos não vazios e únicos.")
        seen.add(code)
        w = d.get("weight_percent")
        if type(w) not in (int, float) or not 0 < w <= 100 or not math.isfinite(w):
            raise InvalidInput("Pesos devem ser números finitos maiores que zero e até 100.")
        weights.append(w)
    if not math.isclose(math.fsum(weights), 100.0, rel_tol=0, abs_tol=0.02):
        raise InvalidInput("Os pesos dos domínios não somam 100%.")
    return weights


def validate_manifest(manifest):
    if not isinstance(manifest, dict):
        raise InvalidInput("O manifesto deve ser um objeto.")
    weights = validate_domains(manifest.get("domains"))
    if not isinstance(manifest.get("exam_code"), str) or not manifest["exam_code"].strip():
        raise InvalidInput("exam_code deve ser texto não vazio.")
    count = manifest.get("exam_questions")
    if type(count) is not int or count < len(weights):
        raise InvalidInput("exam_questions deve permitir ao menos uma questão por domínio.")
    for d in manifest["domains"]:
        if not isinstance(d.get("name"), str) or not d["name"].strip():
            raise InvalidInput("Cada domínio deve ter um nome não vazio.")
    ids = {d["id"] for d in manifest["domains"]}
    for field in ("quick_distribution", "deep_distribution"):
        if field in manifest:
            distribution = manifest[field]
            if (not isinstance(distribution, dict) or set(distribution) != ids
                    or any(type(n) is not int or n < 1 for n in distribution.values())):
                raise InvalidInput(f"{field} deve cobrir exatamente todos os domínios com inteiros positivos.")


def allocate(domains, count):
    weights = validate_domains(domains)
    if type(count) is not int or count < len(domains):
        raise InvalidInput("Quantidade inválida: mínimo de 1 questão por domínio.")
    # Método da maior sobra (Hamilton) sobre o total completo.
    # Se algum peso produzir 0 questões, garantir pelo menos uma por domínio
    # e retirar a compensação de quem ficou mais acima da cota.
    # Normalizar apenas a tolerância de arredondamento; não alterar os pesos da fonte.
    exact = [count * (w / math.fsum(weights)) for w in weights]
    allocated = [math.floor(x) for x in exact]
    unassigned = count - sum(allocated)
    order = sorted(range(len(domains)), key=lambda i: (-(exact[i] - allocated[i]), i))
    for i in order[:unassigned]:
        allocated[i] += 1
    for i, n in enumerate(allocated):
        if n < 1:
            candidates = [j for j, v in enumerate(allocated) if v > 1]
            if not candidates:
                raise InvalidInput("Não há questões suficientes para cobrir todos os domínios.")
            donor = max(candidates, key=lambda j: (allocated[j] - exact[j], allocated[j], -j))
            allocated[donor] -= 1
            allocated[i] = 1
    return {d["id"]: allocated[i] for i, d in enumerate(domains)}


def normalize_choice(value):
    if isinstance(value, str):
        s = value.upper().replace(",", " ").replace("/", " ").strip()
        out = list(s) if len(s) > 1 and " " not in s and all(x in "ABCD" for x in s) else s.split()
    elif isinstance(value, list):
        out = value
    else:
        raise InvalidInput("Resposta e gabarito precisam ser texto ou lista.")
    try:
        normalized = [str(c).strip().upper() for c in out]
    except Exception as exc:
        raise InvalidInput("Resposta não interpretável.") from exc
    if not normalized or any(c not in ("A", "B", "C", "D") for c in normalized):
        raise InvalidInput("As alternativas devem ser A, B, C ou D.")
    if len(set(normalized)) != len(normalized):
        raise InvalidInput("Alternativas repetidas são inválidas.")
    return set(normalized)


def evaluate(manifest, responses):
    validate_manifest(manifest)
    if not isinstance(responses, list):
        raise InvalidInput("O campo 'responses' deve ser uma lista.")
    domains = manifest["domains"]
    weight_total = math.fsum(d["weight_percent"] for d in domains)
    lookup = {d["id"]: d for d in domains}
    grouped = {d["id"]: [] for d in domains}
    seen_ids = set()
    excluded = []
    for pos, r in enumerate(responses, 1):
        if not isinstance(r, dict):
            raise InvalidInput(f"Registro {pos} não é objeto.")
        code = r.get("domain_id")
        if not isinstance(code, str) or code not in lookup:
            raise InvalidInput(f"Domínio inválido no registro {pos}: {code!r}")
        item_id = r.get("id", pos)
        if type(item_id) not in (str, int) or (isinstance(item_id, str) and not item_id.strip()):
            raise InvalidInput(f"ID de questão inválido no registro {pos}.")
        if str(item_id) in seen_ids:
            raise InvalidInput(f"ID de questão duplicado: {item_id}")
        seen_ids.add(str(item_id))
        invalidated = r.get("invalidated", False)
        if type(invalidated) is not bool:
            raise InvalidInput("invalidated deve ser booleano.")
        if invalidated:
            reason = r.get("invalidation_reason")
            if not isinstance(reason, str) or not reason.strip():
                raise InvalidInput("Questão anulada exige invalidation_reason não vazio.")
            excluded.append({"id": item_id, "domain_id": code, "reason": reason})
            continue
        confidence = r.get("confidence")
        if type(confidence) is not int or confidence not in (1, 2, 3):
            raise InvalidInput(f"Confiança inválida na questão {pos}; use 1, 2 ou 3.")
        correct = normalize_choice(r.get("correct"))
        answer = normalize_choice(r.get("answer"))
        if len(correct) > 2 or len(answer) > 2:
            raise InvalidInput(f"Questão {pos}: o formato aceita até 2 alternativas corretas.")
        match = correct == answer
        topic = r.get("topic")
        if topic is None or topic == "":
            topic = "não informado"
        if not isinstance(topic, str):
            raise InvalidInput(f"Tópico inválido na questão {pos}; use texto.")
        grouped[code].append({
            "id": item_id,
            "acerto": match,
            "confianca": confidence,
            "falsa_certeza": (not match and confidence == 3),
            "acerto_com_duvida": (match and confidence == 1),
            "topico": topic,
        })
    results = []
    weighted_sum = 0.0
    covered_weight = 0.0
    for d in domains:
        q = grouped[d["id"]]
        n = len(q)
        ratio = sum(x["acerto"] for x in q) / n if n else None
        accuracy = round(100 * ratio, 2) if n else None
        false_c = sum(x["falsa_certeza"] for x in q)
        low_c = sum(x["acerto_com_duvida"] for x in q)
        if n:
            weighted_sum += float(d["weight_percent"]) * ratio
            covered_weight += float(d["weight_percent"])
        uncertainty = "não medido" if n == 0 else ("alta (amostra pequena)" if n < 3 else "amostra parcial; não é predição")
        # Índice de priorização de estudos, não estimativa de probabilidade de reprovar.
        priority = (round(float(d["weight_percent"]) * (1 - ratio) * (1.5 if false_c else 1), 2) if n else None)
        results.append({
            "domain_id": d["id"], "domain": d["name"], "weight_percent": d["weight_percent"],
            "questions": n, "correct": sum(x["acerto"] for x in q),
            "accuracy_percent": accuracy, "false_certainty_count": false_c,
            "correct_with_low_confidence_count": low_c, "priority_index": priority,
            "uncertainty": uncertainty,
            "error_topics": sorted({x["topico"] for x in q if not x["acerto"]}),
            "observed_topics": sorted({x["topico"] for x in q if x["topico"] != "não informado"}),
        })
    all_covered = all(x["questions"] > 0 for x in results)
    return {
        "exam_code": manifest["exam_code"],
        "skill_version": manifest.get("version"),
        "source_baseline": manifest.get("source_baseline"),
        "questions_answered": len(responses) - len(excluded),
        "questions_submitted": len(responses),
        "questions_invalidated": len(excluded),
        "invalidated_items": excluded,
        "raw_accuracy_percent": round(100 * sum(x["correct"] for x in results) / (len(responses) - len(excluded)), 2) if len(responses) > len(excluded) else None,
        "question_distribution_full_sim": allocate(domains, manifest["exam_questions"]),
        "domain_results": results,
        "covered_domain_weight_percent": round(100 * covered_weight / weight_total, 2),
        "coverage_note": "Peso dos domínios com ao menos um item válido; não mede cobertura de subtópicos nem domínio do conteúdo.",
        "weighted_accuracy_if_all_domains_covered_percent": round(100 * weighted_sum / weight_total, 2) if all_covered else None,
        "note": "Acertos observados em questões simuladas; não equivalem à pontuação oficial escalonada de 720/1000 e não predizem aprovação. Avalie cobertura, consistência, erros graves e simulados completos.",
        "recommendation": "Não recomendar agendamento a partir deste relatório isoladamente; analisar evidências adicionais de domínio e simulados completos.",
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Corrige questões e aloca domínios sem inventar nota de prova.")
    p.add_argument("--manifest", default=str(Path(__file__).resolve().parents[1] / "references" / "dominios.json"))
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", help="JSON contendo {\"responses\":[...]}")
    group.add_argument("--allocate", action="store_true", help="Quantidade por domínio para simulado completo")
    args = p.parse_args(argv)
    try:
        manifest = load_json(args.manifest)
        validate_manifest(manifest)
        if args.allocate:
            result = {"exam_code": manifest["exam_code"], "total": manifest["exam_questions"], "distribution": allocate(manifest["domains"], manifest["exam_questions"])}
        else:
            data = load_json(args.input)
            if not isinstance(data, dict):
                raise InvalidInput("A entrada deve ser um objeto com o campo responses.")
            result = evaluate(manifest, data.get("responses"))
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (ValueError, TypeError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
