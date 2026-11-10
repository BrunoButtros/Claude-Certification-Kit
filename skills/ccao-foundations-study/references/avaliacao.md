# Contrato de avaliação e retomada — v1.0.1

Ler ao corrigir avaliações, anular itens ou exportar/importar progresso. O script é opcional; sem Python, aplicar as mesmas contas manualmente e informar isso. Resolver os caminhos a partir da pasta real da skill, não presumir o diretório de trabalho da conversa.

## Entrada do avaliador

Após encerrar o diagnóstico/simulado, criar um JSON UTF-8 com um objeto `responses`. Exemplo sintético de prática (não é questão de certificação):

```json
{
  "responses": [
    {"id": "q1", "domain_id": "D1", "topic": "tópico do escopo", "correct": "B", "answer": "A", "confidence": 3},
    {"id": "q2", "domain_id": "D1", "topic": "outro tópico", "correct": ["A", "C"], "answer": ["C", "A"], "confidence": 1},
    {"id": "q3", "domain_id": "D2", "invalidated": true, "invalidation_reason": "Duas opções igualmente defensáveis; item excluído após revisão."}
  ]
}
```

- `id`: texto não vazio ou inteiro, único na avaliação. Se ausente, o avaliador usa a posição, mas para histórico persistente sempre fornecer ID explícito.
- `domain_id`: um dos IDs do manifesto desta certificação.
- Itens válidos: `correct`, `answer` e `confidence` obrigatórios. Letras A–D, uma ou duas respostas; a ordem não altera o acerto. Confiança inteira 1–3. Resposta parcial em Choose TWO é erro, sem crédito parcial.
- `topic`: texto opcional; sem ele, a cobertura de tópicos permanece desconhecida. Não inferir um tópico de campos ausentes.
- Anulação: `invalidated: true` exige motivo textual. O item fica no histórico e não entra em nenhuma nota ou contagem de confiança; seu domínio pode passar a não medido. Acrescentar questão substituta com novo ID quando o modo exigir distribuição completa.
- Entradas malformadas devem ser corrigidas; não inventar respostas ou confiança para fazê-las passar no script. Avaliação interrompida não equivale a simulado completo.

Na pasta da skill: `python scripts/avaliar.py --input respostas.json`. De outra pasta, usar caminho absoluto ao script. O manifesto padrão é encontrado em relação ao script; `--manifest` permite escolher explicitamente outro manifesto. A ferramenta de manutenção `tools/avaliar.py` exige `--manifest skills/<nome>/references/dominios.json`.

## Saída

`questions_answered` conta itens válidos submetidos; `questions_submitted` inclui anulados. `raw_accuracy_percent` é o acerto global bruto; `weighted_accuracy_if_all_domains_covered_percent` é o índice ponderado e fica nulo quando falta domínio. `covered_domain_weight_percent` mede somente presença em domínios, não cobertura de todos os tópicos. `observed_topics` lista tópicos informados, sem estimar domínio do conteúdo. Arredondar só na apresentação. Não existe previsão de aprovação nem nota oficial.

Os pesos devem somar 100%; a tolerância numérica máxima é 0,02 ponto percentual. Dentro dessa tolerância, o avaliador normaliza pelo total informado para alocação e percentuais agregados, mantendo intactos os pesos de cada domínio na saída. Isso evita totais superiores a 100% por arredondamento da entrada; a baseline entregue soma exatamente 100%.

## Progresso entre sessões

Usar `assets/progresso-template.json` e o relatório Markdown. O schema 1.1 acrescenta `active_assessment` e `topic_history`; dados 1.0 continuam utilizáveis sem esses campos. Não há armazenamento automático nem importador Python: a skill lê o relatório fornecido pelo estudante e confere certificação/base/versões. Não agregar resultados de avaliações repetidas ou reenviadas em duplicidade.

Em `evaluations`, após encerrar a avaliação, guardar ID da avaliação, modo, data, versões, IDs/enunciados/opções dos itens, gabarito justificado, respostas/confiança, fontes realmente consultadas, anulações e resultado. Em `topic_history`, registrar domínio/tópico, avaliação/item, tipo de erro, revisão e próxima ação; listas vazias significam ausência de evidência. Isso permite revisar erros e evitar repetir questões sem inventar histórico.

Durante diagnóstico/simulado, o gabarito deve ser fixado antes de apresentar cada questão e mantido privado. Não colocar respostas corretas em checkpoints, arquivos ou blocos visíveis ao estudante antes do encerramento. `active_assessment` pode conter ID/modo, data, itens públicos já apresentados e respostas/confiança, posição seguinte e distribuição restante, sem gabarito.

Se o ambiente perder o gabarito privado entre sessões, o histórico público permite retomar estudos, mas não comprova a integridade de uma avaliação em andamento. Marcar como interrompida e iniciar avaliação independente; não recalcular gabaritos retrospectivamente para declarar simulado completo. Exportar correção e histórico completo somente depois de encerrada a avaliação.
