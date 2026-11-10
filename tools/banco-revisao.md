# Banco por domínio, confiança e nova tentativa

Ler antes de montar uma avaliação e ao revisar erros. A aplicação continua sendo conversacional, uma questão por vez.

## Composição da avaliação

`assets/banco-questoes.json` agrupa questões por domínio. O banco Developer começa com cinco questões próprias com revisão documental assistida por IA; os demais bancos começam vazios. Não afirmar que houve revisão independente de especialista ou validação psicométrica. Novos itens podem ser acrescentados após a revisão descrita em `references/qualidade-questoes.md`, com fonte, data e estado de revisão registrados.

Usar `scripts/montar_avaliacao.py --mode quick`, `--mode deep` ou `--mode full` quando houver Python. O script seleciona IDs do banco e reserva vagas para gerar o restante, respeitando as cotas do manifesto; não gera enunciados nem avalia sua validade. `--bank-share 0.5` prefere aproximadamente metade das vagas por domínio do banco, quando houver itens suficientes; é uma escolha pedagógica ajustável, não uma regra oficial. A falta de itens é preenchida por geração, sem duplicar a mesma questão na avaliação ou alterar cotas. Sem Python, aplicar esse procedimento manualmente.

Os itens com estado `documentary_ai_review_no_independent_expert` ou `expert_reviewed` podem ser selecionados; rascunhos ou itens invalidados não entram. Se o estudante já respondeu a uma questão, ela pode reaparecer em outra avaliação para reforço. Informar a repetição, registrar `previously_seen: true` e distinguir acertos em itens novos e repetidos no relatório. Priorizar itens não vistos quando houver alternativas suficientes, sem proibir a revisão dos já conhecidos.

O parâmetro opcional `--seen caminho.json` recebe `{"item_ids": ["ID"]}`. O plano de montagem contém IDs e domínio, nunca gabaritos. Ler internamente a questão do banco selecionada; apresentar apenas enunciado/opções. Gerar e conferir os itens restantes, incluindo Choose TWO na proporção pedagógica da modalidade, levando em conta os formatos já selecionados. Não considerar uma vaga gerada como uma questão pronta antes dessa conferência.

Na pergunta, usar uma etiqueta honesta:

- **Do banco — gerada para estudo; revisão documental por IA**, ou **revisada por especialista**, apenas se esse for de fato o estado registrado.
- **Gerada nesta sessão**, para os itens novos.
- Acrescentar **repetida para revisão** quando já respondida.

Nenhuma das etiquetas significa questão ou gabarito oficial. Não mostrar fontes que revelem a resposta, explicações ou correção antes do encerramento de diagnóstico/simulado. Questões recém-geradas não se tornam automaticamente itens revisados do banco; não modificar o repositório para incorporar perguntas ou respostas do estudante durante o uso.

## Fila de revisão (o “cache” de estudo)

Após corrigir a avaliação, guardar cada erro e cada acerto com confiança 1 na `review_queue` do progresso. O avaliador produz `review_queue_candidates`; são candidatos que a skill completa com o histórico disponível, não um arquivo persistido automaticamente. Guardar:

- ID da avaliação original, ID/versão da questão, domínio e tópico;
- enunciado e todas as alternativas, resposta marcada e gabarito, justificativas e fontes disponíveis;
- confiança original, motivo (`error`, `error_high_confidence` ou `correct_low_confidence`), prioridade e estado;
- referências estudadas e novas tentativas com data, resposta, confiança e explicação do estudante.

Preservar a letra e o texto da alternativa incorreta, além das corretas omitidas em Choose TWO. Se houver acerto parcial, não rotular uma alternativa correta selecionada como errada. Não inventar enunciados ou justificativas ausentes no histórico. Não colocar item anulado na fila como erro; se for anulado depois, marcar a entrada como `invalidated` e tirá-la das prioridades.

Quando o ambiente permitir, salvar o progresso em arquivo da sessão fora da pasta da skill, por exemplo `progresso-estudos/`, e informar o caminho. Não sobrescrever outro histórico sem conferir certificação/avaliação. Sem gravação disponível, manter a fila na conversa e oferecer exportação manual. Ao mudar de conversa, pedir o relatório existente; não afirmar que a fila foi recuperada de memória externa.

## Confiança muda a orientação, nunca a nota de acerto

| Resultado | Orientação |
|---|---|
| Acertou com 1 | Registrar o acerto integral. Revisar o conceito e pedir justificativa: pode ter havido chute ou compreensão ainda insegura. |
| Errou com 1 | Ensinar a base e praticar a distinção entre alternativas antes de avançar. |
| Errou com 3 | Prioridade alta de revisão: explicitar o critério de decisão equivocado, explicar por que a opção marcada falha e trabalhar um contraexemplo. |
| Acertou com 2 ou 3 | Consolidar conforme cobertura e explicação; uma questão isolada não prova domínio. |

Mostrar quantas respostas tiveram confiança 1, quantas foram corretas com dúvida e quantas foram erros com confiança 3, no total e por domínio. Se houver várias respostas 1, inclusive corretas, mencionar o padrão, indicar os assuntos e recomendar estudo e prática para desenvolver compreensão e confiança. Não encerrar com “está bem” só porque o percentual de acertos é alto. Para erros com 3, tratar a falsa certeza explicitamente e sem julgamento pessoal. Não exigir que a pessoa marque 3 na próxima tentativa: o objetivo é justificar a decisão, não aumentar confiança declarada artificialmente.

## Depois do estudo

Fazer explicação curta, indicar a leitura pertinente e um exercício. Ao concluir esse estudo, perguntar **“Pronto para tentar de novo?”** e aguardar a resposta. Se aceitar, reapresentar a questão da fila sem gabarito visível e pedir resposta, confiança e uma justificativa breve. Manter o resultado original e registrar a nova tentativa separadamente; não recalcular a nota do diagnóstico como se o acerto posterior fosse original.

Depois de um acerto explicado, marcar a entrada como `practiced` e oferecer outro cenário do mesmo conceito. Só marcar `understanding_checked` após uma nova aplicação justificada; não declarar retenção de longo prazo com uma única repetição imediata. Se continuar errando ou inseguro, manter a entrada aberta, mudar a explicação e combinar a próxima revisão com o estudante. Não prometer lembretes em segundo plano.
