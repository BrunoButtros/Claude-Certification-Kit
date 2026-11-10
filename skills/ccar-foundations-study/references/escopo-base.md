# Escopo congelado: CCAR-F — 10/11/2026

**Proveniência:** transcrição do documento enviado, não uma atualização do guia oficial. Os domínios e pesos devem ser conferidos no PDF oficial aplicável antes da prova.

## Fatos da prova conforme documento

- 60 questões, 120 minutos, em inglês; aprovação com 720 de 1000.
- Público: arquitetos de solução que desenham, constroem e operam sistemas com agentes Claude em produção.
- As questões partem de cenários de produção (ex.: agente de atendimento, pipeline de revisão de código em CI, sistema multiagente de pesquisa, extração estruturada de documentos) e cobram a decisão de arquitetura mais adequada.

## Domínios, pesos e tópicos — cópia literal da tabela do arquivo

| # | Domínio | Peso | O que cobra |
|---|---|---|---|
| 1 | Agentic Architecture & Orchestration | 27% | Agentic loop e stop_reason; coordenador com subagentes (hub-and-spoke); passar contexto explicitamente aos subagentes; decomposição de tarefas; hooks para regras determinísticas x instrução no prompt; sessões (retomar, bifurcar); critérios de escalonamento para humano |
| 2 | Claude Code Configuration & Workflows | 20% | Hierarquia do CLAUDE.md (usuário, projeto, diretório); regras por caminho; slash commands e Skills; plan mode x execução direta; modo não interativo (-p) em CI com saída estruturada; refinamento iterativo |
| 3 | Prompt Engineering & Structured Output | 20% | Critérios explícitos em vez de instruções vagas; few-shot; tool use com JSON Schema para garantir estrutura; loop de validação e nova tentativa; Message Batches API para cargas sem urgência; revisão em múltiplas passadas |
| 4 | Tool Design & MCP Integration | 18% | Descrição da ferramenta como principal mecanismo de escolha; dividir ou consolidar ferramentas; respostas de erro estruturadas (categoria, se dá para tentar de novo); poucas ferramentas por agente; tool_choice; configuração de servidores MCP no projeto x no usuário; ferramentas nativas (Read, Grep, Glob, Edit) |
| 5 | Context Management & Reliability | 15% | Preservar fatos críticos do caso; perda de informação no meio de contextos longos; aparar saídas de ferramenta; propagação de erro entre agentes; compactação; revisão humana e calibração de confiança; rastreabilidade da fonte (provenance) |

## Política de versão

Não incorporar novos tópicos anunciados em versões posteriores até revisão explícita; marcar divergências conhecidas e data de verificação. Nunca tratar as notas de questões inventadas como pontuação escalonada oficial.
