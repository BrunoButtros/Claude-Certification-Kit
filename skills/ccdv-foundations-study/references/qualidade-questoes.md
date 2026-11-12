# Padrão de qualidade de questões (usar antes de apresentar cada item)

## Processo interno de validação
1. Identificar domínio, subtema exato e competência descrita em `escopo-base.md`.
   Verificar que a questão mede uma decisão relevante do subtema e que as evidências conhecidas sustentam o gabarito; não apresentar curiosidades aleatórias como conteúdo confirmado de exame.
2. Criar cenário em inglês com decisão específica (público, objetivo, restrições e possibilidade de falha); não perguntar apenas definição de termo.
   Variar setores e públicos conforme o domínio: destinatários técnicos e não técnicos, fornecedores, liderança, usuários, compras e auditoria. Usar detalhes que mudem a decisão, sem jargão gratuito ou estereótipos. Conferir finalidade e autorização, em vez de tratar cargo ou palavra-chave como gabarito automático. Ver `references/ingles-cenarios.md`.
3. Formular exatamente 4 opções, A–D. Se `single`, uma alternativa é claramente melhor **dentro das restrições**; se `multi`, exatamente duas são corretas e o enunciado diz 'Choose TWO'.
4. Para cada alternativa, justificar internamente por que é correta/incorreta, com o critério de decisão. Se duas alternativas puderem ser igualmente boas, reescrever antes de mostrar.
5. Distratores próximos e realistas: solução que funciona mas custa mais, não é confiável, viola restrição, ignora governança ou abstrai mecanismo técnico.
6. Não dar pistas por tamanho da alternativa, frases absolutas ou repetição de palavras do enunciado só na resposta certa; posições de gabarito distribuídas de modo não previsível.
7. Não exigir memorização de números voláteis (preços, limites, versões de SDK, tempos de cache) sem evidência primária compatível com a versão do guia.
   Ao usar batches em cenários com prazo, não sugerir que o processamento sempre terminará durante a noite; explicitar tolerância a atrasos, possibilidade de expiração e plano alternativo quando um prazo rígido for relevante.
8. Para cada questão, preparar uma referência ao tópico do guia e, se disponível, link oficial realmente consultado. Sem fonte verificada, usar referência de domínio/subtema e **não inventar link direto**.
   Ao recomendar leitura após um erro, conferir o conteúdo da página e identificar a seção e o conceito que resolve aquele erro. O link deve ser útil para a lacuna específica; não afirmar que uma página genérica cobre um detalhe que não foi localizado. Na ausência de acesso, informar que a pertinência não foi verificada e oferecer explicação própria e exercício.
9. Usar inglês natural e tecnicamente claro. Explicações ao aluno, depois da entrega, em português.
   Na correção, explicar termos de negócio necessários ao cenário e o que o destinatário precisa fazer com a resposta. Distinguir, com a participação do estudante, dificuldade de leitura e lacuna de conceito. Em prática, fazer isso após a tentativa; em diagnóstico/simulado, somente na correção final, sem pistas antecipadas.
10. Reutilizar questões de forma transparente para revisão, preservando IDs/versão e registrando exposição. Permutar letras não torna a questão inédita. Para verificar aplicação além da memória do item, propor depois um novo cenário e explicitar essa diferença.

## Entrada no banco

Questões do banco precisam de domínio/subtema, enunciado/opções, gabarito, justificativa de cada alternativa, referência consultada, data e estado de revisão. Usar `documentary_ai_review_no_independent_expert` para revisão documental assistida por IA; `expert_reviewed` somente após revisão independente de especialista efetivamente realizada. Itens sem revisão ou ambíguos ficam como rascunho ou inválidos, fora da seleção. Não afirmar equivalência com questões oficiais ou validação psicométrica. Seguir `references/banco-revisao.md` ao combinar o banco e questões novas.

## Níveis
- Inicial/intermediário: reconhecer critério-chave e evitar falha comum.
- Nível de prova: escolher a melhor opção sob 2–3 restrições e distratores próximos.
- Avançado: combinar custo, confiabilidade, operação, segurança ou trade-offs interdependentes, sem fugir do escopo.

## Tratamento de incertezas
- Se não puder justificar consistentemente o gabarito, **descarte a pergunta e substitua**.
- Se o usuário contestar o gabarito depois da avaliação, revisar abertamente, admitir ambiguidade e excluir item da pontuação, se necessário; registrar ID e motivo em `invalidated`/`invalidation_reason` e recalcular conforme `references/avaliacao.md`. Não apenas apagar a questão do histórico.
- Se não houver acesso à documentação, não inventar detalhes técnicos nem referências. Priorizar conceitos sustentados pelo escopo da versão-fonte.
