# Claude Certification Study Skills

Quatro skills independentes para apoiar a preparação para certificações Claude. Elas seguem o formato Agent Skills e oferecem diagnóstico, estudo, prática, simulados e planejamento em português brasileiro, com questões em inglês.

| Certificação | Skill |
|---|---|
| Associate – Foundations | `ccao-foundations-study` |
| Developer – Foundations | `ccdv-foundations-study` |
| Architect – Foundations | `ccar-foundations-study` |
| Architect – Professional | `ccar-professional-study` |

## Como usar

No Codex ou em outro agente compatível, solicite que ele use o `SKILL.md` da certificação desejada e suas referências locais. Por exemplo:

> Use `skills/ccdv-foundations-study/SKILL.md` para fazer um diagnóstico rápido da certificação Developer Foundations.

Para instalar no Claude, envie o ZIP individual correspondente na pasta `packages/` pela área de skills do produto. No Claude Code, copie a pasta da skill para `.claude/skills/` do projeto ou para `~/.claude/skills/`.

## O que cada skill oferece

Diagnósticos rápidos e aprofundados, estudo por domínio, questões situacionais, simulados, revisão de erros e um plano adaptável. Os relatórios podem ser copiados para outra conversa; a persistência depende do ambiente usado.

As questões são geradas para estudo e não são oficiais. Os resultados indicam desempenho observado e não preveem aprovação. As skills não devem ser usadas para responder uma prova oficial em andamento ou acessar questões vazadas.

## Conteúdo e atualização

Os domínios e pesos refletem a base de 10/11/2026 e não foram integralmente verificados contra os guias oficiais autenticados. Consulte o guia oficial aplicável antes de se preparar ou agendar uma prova. `references/fontes.md` em cada skill registra as fontes disponíveis.

## Ferramentas

`tools/build_skills.py` regenera as skills e os ZIPs a partir de `tools/baseline.json` e dos recursos compartilhados. Requer Python 3.9 ou superior e usa a biblioteca padrão:

```bash
python tools/build_skills.py
```

Cada skill inclui uma cópia independente de `scripts/avaliar.py`; a execução Python é opcional. Sem ela, o agente pode calcular os resultados manualmente seguindo a metodologia da skill.
