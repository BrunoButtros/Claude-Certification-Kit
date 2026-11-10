# Roteiro de estudo — Developer Foundations

Este mapa relaciona recursos oficiais a tópicos da baseline de 10/11/2026. Os links foram conferidos em 10/11/2026 para a finalidade indicada, mas a documentação pode mudar e não comprova que cada detalhe consta do exame. Consulte o conteúdo antes de afirmar que uma seção específica responde à dúvida; quando não houver navegação disponível, sinalize que a confirmação atual não foi possível.

Os identificadores D1–D8 são rótulos internos desta skill, não uma afirmação sobre a ordem dos domínios no guia oficial. Os tópicos e pesos foram herdados do documento inicial, que cita reproduções de terceiros; a seleção de links e exercícios deste roteiro foi criada para a skill. Nenhuma dessas partes foi cotejada integralmente com o PDF oficial autenticado ou os conteúdos internos das trilhas da Partner Academy.

## Cursos da Partner Academy indicados pelo estudante

- [Trilha Claude Developer](https://anthropic-partners.skilljar.com/path/claude-developer)
- [Trilha Claude Certified Developer – Foundations](https://anthropic-partners.skilljar.com/path/claude-certified-developer-foundations)

São links para a Partner Academy e podem exigir acesso autorizado. As imagens fornecidas pelo estudante mostram o índice resumido abaixo; o conteúdo integral das aulas e o guia oficial autenticado não foram confrontados com a baseline. Não pedir de novo o índice que já foi fornecido nem afirmar que as aulas completas foram lidas. Ver [FAQ de certificações](https://anthropic-partners.skilljar.com/page/faq-certifications) quanto à elegibilidade atual.

### Índice de preparação fornecido em imagens — 10/11/2026

| Bloco visto na trilha | Temas indicados no resumo exibido |
|---|---|
| MSO Foundations | Fundamentos de modelos e conceitos técnicos usados pelo restante do curso |
| Production-Grade Prompting, Agents & Tool Use | Prompts, ferramentas, contexto e agent loops em integrações |
| Claude Code, MCP & Integration | Integrações configuráveis, compartilháveis e seguras |
| Production Engineering, Evals & Security | Avaliar um agente e prepará-lo para tráfego de produção |
| Accelerators & IP Contribution | Reutilização, revisão e entrega de uma solução além do projeto inicial |

As outras imagens mostram a trilha geral Developer: fundamentos e limitações de IA, AI Fluency for Builders, plataforma e modelos, escolha de modelo, Claude Platform 101, Claude Code 101/in action, MCP, skills e subagentes. O índice de cursos não substitui o blueprint da prova nem altera os pesos congelados. Usar esse índice salvo para orientar a navegação na Academy, sem pesquisar ou reconstruí-lo a cada conversa.

## Material de estudo já salvo na skill

`references/guia-estudo.md` contém a teoria dos oito domínios, exemplos e exercícios respondidos na conversa. Para um pedido de conteúdo completo, disponibilizar esse arquivo e seu índice; para uma dúvida, localizar a seção pertinente e explicar aqui. Não recriar uma apostila, aplicativo ou programa de laboratório. Os links abaixo são complementos para aprofundar ou conferir uma dúvida, não uma exigência de navegação antes de mostrar o material salvo.

## Vídeos oficiais como apoio

O [canal Claude](https://www.youtube.com/@claude) também é um recurso de estudo. A seleção salva em `references/videos-estudo.md` reúne cinco vídeos publicados por Anthropic, com associação ao guia, capítulos públicos quando disponíveis e perguntas para responder depois. Ela cobre prompts, agentes, MCP e Claude Code. Não afirmar que já existe uma seleção específica suficiente para todos os domínios.

Usar a sequência **ler o conceito → assistir ao trecho pertinente, se desejar → explicar a decisão aqui → praticar ou tentar novamente**. A curadoria não equivale a ter assistido aos vídeos: informa claramente onde a identificação se apoia em descrição/capítulos e onde só há título/contexto. Não usar um vídeo genérico como referência garantida para um erro sobre caching, streaming, batches, segurança ou avaliação.

## Leituras por domínio

| Domínio da baseline | O que explorar | Recurso e utilidade |
|---|---|---|
| D1 Applications & Integration | Messages API, streaming, erros, cache e batches | [Messages API](https://platform.claude.com/docs/en/api/messages); [streaming](https://platform.claude.com/docs/en/build-with-claude/streaming); [batches](https://platform.claude.com/docs/en/build-with-claude/batch-processing); [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching). Cada página explica um mecanismo diferente de integração. |
| D2 Model Selection & Optimization | Modelos, custo, latência, batches e cache | [Visão geral de modelos](https://platform.claude.com/docs/en/models/overview) e as páginas de batches e caching acima, para comparar capacidades e mecanismos de otimização. Não congelar nomes ou preços atuais como conteúdo de prova. |
| D3 Agents & Workflows | Etapas fixas, roteamento e decomposição dinâmica | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), em especial as seções sobre prompt chaining e orchestrator-workers. O artigo sinaliza que partes do ecossistema evoluíram. |
| D4 Prompt & Context Engineering | Critérios, exemplos, estrutura e contexto | [Visão geral de prompt engineering](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview), ponto de partida para as técnicas de prompting. |
| D5 Tools & MCPs | Chamada e retorno de ferramentas; resources, tools e prompts | [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) e [conceitos de servidor MCP](https://modelcontextprotocol.io/docs/learn/server-concepts). |
| D6 Security & Safety | Injeção de prompt, menor privilégio e revisão humana | [Mitigação de prompt injection](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks), para entender a ameaça e os controles. |
| D7 Claude Code | Configuração e fluxos de trabalho | [Visão geral do Claude Code](https://code.claude.com/docs/en/overview), ponto de entrada para a documentação de configuração e fluxos. |
| D8 Evaluation, Testing & Debugging | Critérios de sucesso, avaliações e regressão | [Construção de avaliações](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests), para definir critérios e casos de teste. |

## Uso após diagnóstico

Associe cada erro ao trecho da documentação que explica a decisão, e não apenas a uma página sobre o domínio. Por exemplo: etapas fixas versus decomposição dinâmica → seções de padrões no artigo sobre agentes; relatórios assíncronos → batches; diferença de prefixo → caching; entrega incremental → streaming. Mostre qual pergunta a leitura responde e proponha um pequeno exercício antes de reaplicar um cenário novo. Um link, por si só, não garante aprendizagem ou validade do gabarito.
