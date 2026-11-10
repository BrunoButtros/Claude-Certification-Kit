# Contrato de avaliação e retomada — v1.1.0

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
- `question` e `options`: campos opcionais para preservar o enunciado e os textos de A–D nos candidatos da fila; preencher com o item realmente apresentado, sem reconstrução inventada. Sem esses campos, o avaliador retorna as letras e a skill deve recuperar os textos do histórico ou do banco pela versão correta.
- `previously_seen`: booleano opcional, padrão `false`; usar `true` se o estudante já respondeu ao mesmo item em outra avaliação. Não duplicar o ID dentro da avaliação atual. Informar acertos em itens novos e repetidos separadamente.
- Anulação: `invalidated: true` exige motivo textual. O item fica no histórico e não entra em nenhuma nota ou contagem de confiança; seu domínio pode passar a não medido. Acrescentar questão substituta com novo ID quando o modo exigir distribuição completa.
- Entradas malformadas devem ser corrigidas; não inventar respostas ou confiança para fazê-las passar no script. Avaliação interrompida não equivale a simulado completo.

Na pasta da skill: `python scripts/avaliar.py --input respostas.json`. De outra pasta, usar caminho absoluto ao script. O manifesto padrão é encontrado em relação ao script; `--manifest` permite escolher explicitamente outro manifesto. A ferramenta de manutenção `tools/avaliar.py` exige `--manifest skills/<nome>/references/dominios.json`.

## Saída

`questions_answered` conta itens válidos submetidos; `questions_submitted` inclui anulados. `raw_accuracy_percent` é o acerto global bruto; `weighted_accuracy_if_all_domains_covered_percent` é o índice ponderado e fica nulo quando falta domínio. `covered_domain_weight_percent` mede somente presença em domínios, não cobertura de todos os tópicos. `observed_topics` lista tópicos informados, sem estimar domínio do conteúdo. Arredondar só na apresentação. Não existe previsão de aprovação nem nota oficial.

`confidence_summary` conta questões e acertos para confiança 1, 2 e 3. Cada domínio traz `low_confidence_count` e `review_topics`, incluindo acertos com dúvida. `exposure_summary` separa resultados em itens novos e já vistos.

`confidence_guidance` explicita as ações recomendadas para confiança 1 e erros com confiança 3, com contagens e tópicos. Usar esses sinais no plano mesmo quando `priority_index` é zero por todos os acertos terem sido corretos.

`review_queue_candidates` contém todos os erros e acertos com confiança 1, com ID, domínio, tópico, resposta, gabarito, alternativas incorretas selecionadas e corretas omitidas. Erros com confiança 3 recebem prioridade alta. É saída para uso após o encerramento da avaliação; não exibi-la antecipadamente nem afirmar que ela foi salva automaticamente. A skill deve associar os candidatos ao histórico completo para formar a fila de revisão descrita em `references/banco-revisao.md`.

Os pesos devem somar 100%; a tolerância numérica máxima é 0,02 ponto percentual. Dentro dessa tolerância, o avaliador normaliza pelo total informado para alocação e percentuais agregados, mantendo intactos os pesos de cada domínio na saída. Isso evita totais superiores a 100% por arredondamento da entrada; a baseline entregue soma exatamente 100%.

## Progresso entre sessões

Usar `assets/progresso-template.json` e o relatório Markdown. O schema 1.2 acrescenta `review_queue`; schemas 1.0/1.1 continuam legíveis sem inventar a fila ou o histórico ausentes. Não há armazenamento automático nem importador Python: a skill lê o relatório fornecido pelo estudante e confere certificação/base/versões. Não agregar resultados de avaliações repetidas ou reenviadas em duplicidade. As novas tentativas da fila pertencem à revisão; o resultado da avaliação original permanece preservado.

Em `evaluations`, após encerrar a avaliação, guardar ID da avaliação, modo, data, versões, IDs/enunciados/opções dos itens, gabarito justificado, respostas/confiança, fontes realmente consultadas, anulações e resultado. Em `topic_history`, registrar domínio/tópico, avaliação/item, tipo de erro, revisão e próxima ação; listas vazias significam ausência de evidência. Isso permite revisar erros e evitar repetir questões sem inventar histórico.

Durante diagnóstico/simulado, o gabarito deve ser fixado antes de apresentar cada questão e mantido privado. Não colocar respostas corretas em checkpoints, arquivos ou blocos visíveis ao estudante antes do encerramento. `active_assessment` pode conter ID/modo, data, itens públicos já apresentados e respostas/confiança, posição seguinte e distribuição restante, sem gabarito.

Se o ambiente perder o gabarito privado entre sessões, o histórico público permite retomar estudos, mas não comprova a integridade de uma avaliação em andamento. Marcar como interrompida e iniciar avaliação independente; não recalcular gabaritos retrospectivamente para declarar simulado completo. Exportar correção e histórico completo somente depois de encerrada a avaliação.
