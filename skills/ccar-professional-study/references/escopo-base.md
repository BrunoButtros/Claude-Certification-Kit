# Escopo congelado: CCAR-P — 10/11/2026

**Proveniência:** transcrição do documento enviado, não uma atualização do guia oficial. Os domínios e pesos devem ser conferidos no PDF oficial aplicável antes da prova.

## Fatos da prova conforme documento

- 63 questões, 120 minutos, em inglês, múltipla escolha e múltipla resposta; aprovação com 720 de 1000.
- Público: arquitetos e líderes técnicos que respondem de ponta a ponta por soluções Claude em produção, da descoberta à operação.
- A CCAR-F não é pré-requisito, mas a prova assume esse conhecimento.
- Questões de cenário corporativo: cobram trade-offs entre negócio, risco, custo e operação.

## Domínios, pesos e tópicos — cópia literal da tabela do arquivo

| # | Domínio | Peso | O que cobra |
|---|---|---|---|
| 1 | Solution Design & Architecture | 17% | Ligar decisões de arquitetura a resultados de negócio mensuráveis; fluxo ponta a ponta (entrada, processamento, saída, feedback); escolher entre workflow, agente, LLM aumentado ou multiagente; decompor problemas e orquestrar ferramentas e agentes |
| 2 | Claude Models, Prompting & Context Engineering | 13% | Trade-offs de modelo (complexidade, qualidade, velocidade, tamanho de contexto, custo); system prompts, templates, zero-shot, few-shot, raciocínio estruturado, guardrails; gestão de contexto e tokens com prompt caching, prompts modulares e Skills |
| 3 | Integration | 19% | Menor privilégio para ferramentas e agentes; pipeline de geração aumentada por recuperação (RAG): chunking, indexação, recuperação; escolher entre MCP, APIs, CLIs e comunicação agente-agente; observabilidade; descoberta progressiva x contexto monolítico grande |
| 4 | Evaluation, Testing & Optimization | 16% | Métricas de precisão, latência, custo, segurança; datasets de avaliação com revisão automática e humana; teste A/B; diagnóstico de alucinação, falha de prompt e modelo inadequado; monitoramento para otimizar tokens, tempo de resposta e custo |
| 5 | Governance, Safety & Risk Management | 14% | Guardrails contra mau uso e modos de falha; revisão humana (human-in-the-loop) para saídas sensíveis ou de alto impacto; conformidade (GDPR, HIPAA, FedRAMP, e no Brasil a LGPD); viés, equidade, transparência, privacidade |
| 6 | Stakeholder Communication & Lifecycle Management | 14% | Descoberta estruturada e levantamento de requisitos; explicar decisões e trade-offs para público técnico e não técnico; documentação; gerir feedback do desenho à melhoria contínua |
| 7 | Developer Productivity & Operational Enablement | 7% | Configurar Claude Code e ambientes compartilhados de equipe; fluxos de código, teste e documentação assistidos por IA; usar Claude para depurar e apoiar a operação em produção |

## Política de versão

Não incorporar novos tópicos anunciados em versões posteriores até revisão explícita; marcar divergências conhecidas e data de verificação. Nunca tratar as notas de questões inventadas como pontuação escalonada oficial.
