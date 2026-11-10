# Claude Certified Architect – Foundations (CCAR-F)

Esta certificação integra o programa da Anthropic para organizações parceiras. Confirme elegibilidade e acesso na [FAQ oficial](https://anthropic-partners.skilljar.com/page/faq-certifications); estudar com esta skill não exige informar empresa ou e-mail.

## Conteúdo desta preparação

Base de conteúdo: 10/11/2026. Os domínios e pesos abaixo são os da baseline, ainda não integralmente conferida com o guia oficial autenticado.

| Domínio | Peso | Assuntos |
|---|---:|---|
| Agentic Architecture & Orchestration | 27% | Agentic loop e stop_reason; coordenador com subagentes (hub-and-spoke); passar contexto explicitamente aos subagentes; decomposição de tarefas; hooks para regras determinísticas x instrução no prompt; sessões (retomar, bifurcar); critérios de escalonamento para humano |
| Claude Code Configuration & Workflows | 20% | Hierarquia do CLAUDE.md (usuário, projeto, diretório); regras por caminho; slash commands e Skills; plan mode x execução direta; modo não interativo (-p) em CI com saída estruturada; refinamento iterativo |
| Prompt Engineering & Structured Output | 20% | Critérios explícitos em vez de instruções vagas; few-shot; tool use com JSON Schema para garantir estrutura; loop de validação e nova tentativa; Message Batches API para cargas sem urgência; revisão em múltiplas passadas |
| Tool Design & MCP Integration | 18% | Descrição da ferramenta como principal mecanismo de escolha; dividir ou consolidar ferramentas; respostas de erro estruturadas (categoria, se dá para tentar de novo); poucas ferramentas por agente; tool_choice; configuração de servidores MCP no projeto x no usuário; ferramentas nativas (Read, Grep, Glob, Edit) |
| Context Management & Reliability | 15% | Preservar fatos críticos do caso; perda de informação no meio de contextos longos; aparar saídas de ferramenta; propagação de erro entre agentes; compactação; revisão humana e calibração de confiança; rastreabilidade da fonte (provenance) |

## Materiais para estudar

- [Escopo por domínio](escopo-base.md).
- [Fontes de referência](fontes.md).
- [Certificações e preparação na Partner Academy](https://anthropic-partners.skilljar.com/page/partner-certifications).

Os links fazem parte do material salvo; sua presença não significa que foram consultados nesta sessão. Os cursos da Partner Academy podem exigir acesso autorizado.

Vamos estudar e responder questões aqui na conversa. As questões são próprias de estudo, com origem identificada; não são itens oficiais. A pontuação escalonada oficial não pode ser convertida diretamente em percentual de acertos.

**Gostaria de fazer um teste para medir seu conhecimento atual?**
Opções: 12 questões, 25 questões ou simulado de 60, conforme a baseline. Antes de começar, vamos considerar sua disponibilidade semanal e eventual data-alvo.
