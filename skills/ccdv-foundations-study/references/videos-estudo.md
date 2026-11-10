# Vídeos de apoio — Developer Foundations

Canal indicado: [Claude no YouTube](https://www.youtube.com/@claude). Os vídeos abaixo aparecem publicados por Anthropic nas páginas públicas consultadas em **10/11/2026**. A curadoria usa títulos, descrições e capítulos públicos; os vídeos não foram assistidos integralmente nem tiveram suas transcrições revisadas. Os objetivos e exercícios são propostas pedagógicas desta skill, não citações dos vídeos.

São complementos ao guia salvo e às referências técnicas. Não substituem os cursos da Partner Academy nem confirmam cobertura do exame. Foram publicados em 2024/2025: detalhes de produto podem ter mudado. Um tema novo apresentado em um vídeo não passa automaticamente a integrar a baseline.

## Escolher pelo assunto

| Assunto do guia | Recurso selecionado | Finalidade no estudo |
|---|---|---|
| D1 Integração e D5 Tools & MCPs | [V1 — Building with MCP and the Claude API](https://www.youtube.com/watch?v=aZLr962R6Ag) | Entender a relação entre contexto, ferramentas e integração MCP/API. Não é uma aula específica de caching, streaming ou batches. |
| D3 Agents & Workflows | [V2 — Building more effective AI agents](https://www.youtube.com/watch?v=uhJJgc-0iTQ) | Discutir simplicidade, coordenação e falhas de sistemas agentic. |
| D4 Prompt & Context Engineering | [V3 — AI prompt engineering: A deep dive](https://www.youtube.com/watch?v=T9aRN5JkmL8) | Estudar o processo de refinar prompts e critérios de qualidade. |
| D7 Claude Code | [V4 — Claude Code best practices — Code w/ Claude](https://www.youtube.com/watch?v=gv0WHhKelSE) | Conhecer práticas de uso; conferir detalhes de configuração na documentação atual. |
| D7 Claude Code em CI | [V5 — Building headless automation with Claude Code — Code w/ Claude](https://www.youtube.com/watch?v=dRsjO-88nBs) | Introduzir automação sem interface interativa, como assunto de estudo. |

Para D2 (modelos e otimização), D6 (segurança) e D8 (avaliações), esta edição ainda não seleciona um vídeo específico que cubra suficientemente os assuntos. Usar as explicações e leituras do guia, em vez de indicar um vídeo genérico como se resolvesse qualquer dúvida. O mesmo vale para detalhes de cache, batches e streaming.

## V1 — MCP e Claude API

[Building with MCP and the Claude API](https://www.youtube.com/watch?v=aZLr962R6Ag) — publicado em 09/10/2025.

**No guia:** capítulos 1, 3 e 5; especialmente 5.4 e 5.5. A descrição pública apresenta MCP, integração com a API e gestão de contexto/ferramentas. Os capítulos indicam [introdução a MCP, 00:30](https://www.youtube.com/watch?v=aZLr962R6Ag&t=30s), [conector na API, 10:40](https://www.youtube.com/watch?v=aZLr962R6Ag&t=640s) e [contexto e ferramentas, 14:20](https://www.youtube.com/watch?v=aZLr962R6Ag&t=860s).

**Antes:** explique com suas palavras o que o modelo recebe e qual componente executa uma ferramenta.

**Depois, responda aqui:** um servidor oferece um manual como contexto e uma ação para abrir um chamado. Como você separaria as duas capacidades? Quem deve verificar a autorização da ação?

**Como conferir:** comparar a resposta com os contratos de tools/resources/prompts do capítulo 5 e com a documentação MCP. A sugestão de revisão é nossa; não afirmar que o vídeo contém essa pergunta ou sua resposta literal.

## V2 — Agentes e escolha de arquitetura

[Building more effective AI agents](https://www.youtube.com/watch?v=uhJJgc-0iTQ) — publicado em 17/10/2025.

**No guia:** capítulos 3.1–3.4. A descrição pública aborda evolução dos agentes, padrões multiagente e ferramentas. Os capítulos indicam [workflows e agentes, 06:40](https://www.youtube.com/watch?v=uhJJgc-0iTQ&t=400s), [arquiteturas simples, 08:30](https://www.youtube.com/watch?v=uhJJgc-0iTQ&t=510s), [orquestração e subagentes, 09:30](https://www.youtube.com/watch?v=uhJJgc-0iTQ&t=570s) e [falhas comuns, 14:15](https://www.youtube.com/watch?v=uhJJgc-0iTQ&t=855s).

**Antes:** descreva a diferença entre uma sequência fixa e um trabalho cuja decomposição ainda precisa ser descoberta.

**Depois, responda aqui:** no fluxo extrair → validar → resumir, que decisão realmente exigiria autonomia? Em que mudança do problema você passaria a considerar orchestrator-workers?

**Como conferir:** justificar pelas dependências e pela variabilidade do trabalho. Usar também o artigo [Building effective agents](https://www.anthropic.com/research/building-effective-agents), que descreve prompt chaining. O vídeo complementa a discussão; o artigo sustenta a comparação específica entre padrões.

## V3 — Refinamento de prompts

[AI prompt engineering: A deep dive](https://www.youtube.com/watch?v=T9aRN5JkmL8) — publicado em 05/09/2024.

**No guia:** capítulos 4.1–4.4. A descrição aborda evolução do prompting e dicas práticas. Os capítulos indicam [definição, 02:05](https://www.youtube.com/watch?v=T9aRN5JkmL8&t=125s), [refinamento, 12:17](https://www.youtube.com/watch?v=T9aRN5JkmL8&t=737s) e [prática de prompting, 50:52](https://www.youtube.com/watch?v=T9aRN5JkmL8&t=3052s).

**Antes:** escolha uma tarefa e diga como reconheceria uma resposta boa ou ruim.

**Depois, responda aqui:** reescreva “classifique este ticket corretamente”, acrescentando categorias, evidência necessária, tratamento de dúvida e formato de saída. Proponha um caso que exponha uma ambiguidade.

**Como conferir:** verificar se o contrato é observável e se o exemplo esclarece a decisão. A publicação é anterior à baseline; detalhes sobre modelos ou técnicas devem ser conferidos na referência técnica aplicável.

## V4 — Práticas de Claude Code

[Claude Code best practices — Code w/ Claude](https://www.youtube.com/watch?v=gv0WHhKelSE) — publicado em 31/07/2025; a descrição informa apresentação no evento de 22/05/2025.

**No guia:** capítulos 7.1–7.4. A página consultada confirma título, publicação e contexto do evento. Não há nesta curadoria transcrição ou capítulos que permitam indicar um minuto específico.

**Antes:** diferencie instrução em CLAUDE.md de uma permissão efetiva de execução.

**Depois, responda aqui:** uma equipe quer convenções compartilhadas e bloqueio de implantação. Que papel cabe às instruções e que papel cabe às permissões? Não é necessário instalar ou executar Claude Code para responder.

**Como conferir:** usar o capítulo 7 e a documentação de [memória](https://code.claude.com/docs/en/memory) e [permissões](https://code.claude.com/docs/en/permissions). Não atribuir ao vídeo uma orientação específica sem localizar o trecho correspondente.

## V5 — Automação headless como conceito

[Building headless automation with Claude Code — Code w/ Claude](https://www.youtube.com/watch?v=dRsjO-88nBs) — publicado em 31/07/2025; a descrição informa apresentação no evento de 22/05/2025.

**No guia:** capítulo 7.5. A indicação se baseia no título e na descrição pública do evento; não foram revisados os comandos demonstrados. Não há timestamp validado nesta curadoria.

**Antes:** explique o que muda entre conversar com uma ferramenta e chamá-la em um job automatizado.

**Depois, responda aqui:** descreva entrada, ferramentas permitidas, contrato da saída e tratamento de falhas de um job fictício de revisão. O exercício é respondido no chat; o vídeo não cria obrigação de programar um simulador.

**Como conferir:** comparar com o capítulo 7.5 e a [documentação de execução programática](https://code.claude.com/docs/en/headless). Não copiar comandos de uma demonstração antiga sem verificar sua versão.

## Como usar durante a tutoria

Sugerir um vídeo pertinente por vez, dizendo por que vale vê-lo, qual trecho foi identificado e qual pergunta o estudante deverá conseguir responder. Depois da leitura ou vídeo, discutir a resposta na conversa e oferecer a nova tentativa da fila de revisão. Se não houve acesso à transcrição ou ao trecho, não afirmar que o vídeo garante a correção de um erro específico. Para parâmetros exatos e regras de API, usar a documentação, não o título de um vídeo como evidência de gabarito.

Os links e esta curadoria estão salvos na skill: não pesquisar o canal novamente só para reproduzir a lista. Verificar atualizações apenas quando houver link quebrado, divergência concreta, dúvida não coberta ou pedido do estudante.
