# Escopo congelado: CCDV-F — 10/11/2026

**Proveniência:** transcrição do documento enviado, não uma atualização do guia oficial. Os domínios e pesos devem ser conferidos no PDF oficial aplicável antes da prova.

## Fatos da prova conforme documento

- 53 questões, 120 minutos, em inglês, múltipla escolha e múltipla resposta; aprovação com 720 de 1000.
- Público: desenvolvedores e engenheiros de IA que constroem aplicações, agentes, integrações e pipelines com a Claude API.
- Questões de cenário: cobram a melhor decisão técnica, inclusive detalhes exatos da API.

## Domínios, pesos e tópicos — cópia literal da tabela do arquivo

| # | Domínio | Peso | O que cobra |
|---|---|---|---|
| 1 | Applications & Integration | 33,1% | Messages API (roles, system, max_tokens, stop_reason), streaming, tratamento de erros e retries (429, 529), prompt caching (cache_control, tempo de vida do cache), Message Batches API, structured outputs, extended thinking, SDKs, Files API, desenho de aplicação por interface |
| 2 | Model Selection & Optimization | 16,8% | Opus x Sonnet x Haiku por qualidade, latência e custo; janela de contexto; redução de custo e latência com caching, batches e roteamento entre modelos |
| 3 | Agents & Workflows | 14,7% | Agentic loop guiado por stop_reason; padrões de workflow (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer); quando usar workflow x agente; subagentes; Claude Agent SDK |
| 4 | Prompt & Context Engineering | 11% | System prompt, tags XML, few-shot, raciocínio passo a passo, posicionamento em contexto longo, gestão e compactação de contexto |
| 5 | Tools & MCPs | 10,6% | Definição de ferramenta com JSON Schema, descrições, tool_choice, chamadas paralelas, tool_result com is_error; Model Context Protocol (MCP): tools, resources, prompts e transportes |
| 6 | Security & Safety | 8,1% | Injeção de prompt (prompt injection), menor privilégio, dados pessoais, guardrails, aprovação humana para ações de risco |
| 7 | Claude Code | 3,1% | CLAUDE.md, permissões, slash commands, hooks, modo não interativo (-p) em CI |
| 8 | Evaluation, Testing & Debugging | 2,6% | Conjuntos de avaliação, LLM como juiz (LLM-as-judge), testes de regressão de prompt, depuração de respostas |

## Política de versão

Não incorporar novos tópicos anunciados em versões posteriores até revisão explícita; marcar divergências conhecidas e data de verificação. Nunca tratar as notas de questões inventadas como pontuação escalonada oficial.
