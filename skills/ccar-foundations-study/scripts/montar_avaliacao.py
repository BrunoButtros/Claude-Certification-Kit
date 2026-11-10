"""Seleciona IDs do banco e reserva vagas por domínio para questões novas.

A saída não contém gabaritos. A skill apresenta os itens selecionados e cria
somente os que faltarem, seguindo o escopo e o padrão de qualidade.
"""
import argparse
import json
import math
import random
import sys
from pathlib import Path

from avaliar import InvalidInput, allocate, load_json, normalize_choice, validate_manifest


def validate_bank(manifest, bank):
    validate_manifest(manifest)
    if not isinstance(bank, dict) or bank.get("exam_code") != manifest["exam_code"]:
        raise InvalidInput("O banco deve pertencer à certificação do manifesto.")
    if bank.get("baseline") != manifest.get("source_baseline"):
        raise InvalidInput("A base do banco difere da base do manifesto.")
    groups = bank.get("domains")
    ids = {d["id"] for d in manifest["domains"]}
    if not isinstance(groups, dict) or not set(groups) <= ids:
        raise InvalidInput("Domínios do banco inválidos.")
    seen = set()
    for code, items in groups.items():
        if not isinstance(items, list):
            raise InvalidInput("Cada domínio do banco deve conter uma lista.")
        for item in items:
            if not isinstance(item, dict) or item.get("domain_id") != code:
                raise InvalidInput("Questão fora do domínio indicado.")
            key = item.get("id")
            if not isinstance(key, str) or not key.strip() or key in seen:
                raise InvalidInput("IDs do banco devem ser textos únicos e não vazios.")
            seen.add(key)
            for field in ("question", "topic", "source_url", "source_checked", "review_status"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    raise InvalidInput(f"Questão {key}: campo {field} ausente ou inválido.")
            if item.get("origin") != "generated_for_practice":
                raise InvalidInput("O banco atual aceita apenas questões próprias de estudo.")
            for field in ("options", "explanations"):
                content = item.get(field)
                if (not isinstance(content, dict) or set(content) != set("ABCD")
                        or any(not isinstance(v, str) or not v.strip() for v in content.values())):
                    raise InvalidInput(f"Questão {key}: {field} deve cobrir A–D.")
            if len(normalize_choice(item.get("correct"))) > 2:
                raise InvalidInput("O banco aceita escolha simples ou Choose TWO.")


def assemble(manifest, bank, mode="quick", bank_share=0.5, seed=None, seen_ids=None):
    validate_bank(manifest, bank)
    if type(bank_share) not in (float, int) or not math.isfinite(bank_share) or not 0 <= bank_share <= 1:
        raise InvalidInput("bank-share deve estar entre 0 e 1.")
    if mode == "quick":
        quotas = manifest["quick_distribution"]
    elif mode == "deep":
        quotas = manifest["deep_distribution"]
    elif mode == "full":
        quotas = allocate(manifest["domains"], manifest["exam_questions"])
    else:
        raise InvalidInput("Modo inválido; use quick, deep ou full.")
    if seen_ids is None:
        seen_ids = []
    if not isinstance(seen_ids, list) or any(not isinstance(x, str) for x in seen_ids):
        raise InvalidInput("item_ids deve ser uma lista de IDs textuais.")
    seen = set(seen_ids)
    rng = random.Random(seed)
    pending = {}
    for code, quota in quotas.items():
        # Metade é uma preferência pedagógica ajustável, não uma proporção oficial.
        limit = math.ceil(quota * bank_share)
        candidates = [x for x in bank["domains"].get(code, [])
                      if x["review_status"] in ("documentary_ai_review_no_independent_expert", "expert_reviewed")]
        rng.shuffle(candidates)
        candidates.sort(key=lambda x: x["id"] in seen)
        selected = candidates[:limit]
        slots = [{"kind": "bank", "domain_id": code, "bank_id": x["id"],
                  "previously_seen": x["id"] in seen, "topic": x["topic"],
                  "review_status": x["review_status"]} for x in selected]
        slots += [{"kind": "generate", "domain_id": code} for _ in range(quota - len(slots))]
        rng.shuffle(slots)
        pending[code] = slots
    # Intercalar domínios preserva as cotas sem repetir um item na mesma avaliação.
    items = []
    while any(pending.values()):
        for code in quotas:
            if pending[code]:
                slot = pending[code].pop()
                slot["position"] = len(items) + 1
                items.append(slot)
    bank_n = sum(x["kind"] == "bank" for x in items)
    return {"exam_code": manifest["exam_code"], "mode": mode, "total": len(items),
            "distribution": quotas, "from_bank": bank_n, "to_generate": len(items) - bank_n,
            "previously_seen_count": sum(x.get("previously_seen", False) for x in items),
            "items": items,
            "note": "Questões próprias de estudo. O plano preserva a distribuição; não valida a qualidade pedagógica nem gera questões. Não mostrar gabaritos durante a aplicação."}


def main(argv=None):
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(root / "references/dominios.json"))
    parser.add_argument("--bank", default=str(root / "assets/banco-questoes.json"))
    parser.add_argument("--mode", choices=("quick", "deep", "full"), default="quick")
    parser.add_argument("--bank-share", type=float, default=0.5)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--seen", help='JSON com {"item_ids": ["ID"]} de questões já vistas')
    args = parser.parse_args(argv)
    try:
        history = load_json(args.seen) if args.seen else {"item_ids": []}
        if not isinstance(history, dict):
            raise InvalidInput("O histórico deve ser um objeto com item_ids.")
        result = assemble(load_json(args.manifest), load_json(args.bank), args.mode,
                          args.bank_share, args.seed, history.get("item_ids"))
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
