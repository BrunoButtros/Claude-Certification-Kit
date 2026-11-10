# Roteiro de estudo — Developer Foundations

Este mapa relaciona recursos oficiais a tópicos da baseline de 10/11/2026. Os links foram conferidos em 10/11/2026 para a finalidade indicada, mas a documentação pode mudar e não comprova que cada detalhe consta do exame. Consulte o conteúdo antes de afirmar que uma seção específica responde à dúvida; quando não houver navegação disponível, sinalize que a confirmação atual não foi possível.

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
