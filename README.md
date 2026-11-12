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

Ao escolher uma certificação, o tutor apresenta os domínios e recursos de estudo antes de oferecer o diagnóstico. Antes da primeira questão do diagnóstico, pergunta sua disponibilidade semanal e eventual data-alvo para orientar o plano; você pode continuar mesmo sem esses dados. Se pedir diretamente outro modo, ele começa pelo modo solicitado. Após o diagnóstico, o tutor explica os erros, relaciona leituras pertinentes às lacunas e propõe a sequência de revisão e prática.

Cada skill inclui uma apresentação pronta em `references/inicio.md`. A Developer também traz o guia teórico em `references/guia-estudo.md`, para consultar e estudar sem gerar uma nova apostila a cada conversa. A teoria salva segue a baseline; detalhes de versões e requisitos atuais devem ser conferidos quando relevantes.

As quatro skills trazem `references/ingles-cenarios.md`, com vocabulário de negócio, leitura de públicos e objetivos e cinco casos guiados. Esse apoio ajuda a distinguir dificuldade de inglês de lacuna no conceito; explicações contextuais aparecem após a tentativa na prática ou na correção final dos diagnósticos e simulados.

Para quem prefere vídeo, a Developer inclui uma seleção de publicações da Anthropic em `references/videos-estudo.md`, com relação aos assuntos, capítulos públicos quando identificados e exercícios de revisão. Os vídeos complementam a teoria e a documentação; a curadoria explicita o que foi consultado e não pressupõe reprodução integral ou cobertura oficial da prova.

As aulas, os exercícios e as provas acontecem na conversa. Os scripts fornecidos são auxiliares internos opcionais de cálculo e seleção de itens; não é necessário executar um simulador ou programa para estudar ou responder às questões.

Para Developer Foundations, as opções são 16 questões, 32 questões ou um simulado de 53 questões conforme a baseline. A distribuição usa os pesos da baseline como aproximação e não é uma contagem oficial por domínio. A certificação pertence ao programa da Anthropic para parceiros; confirme elegibilidade e acesso na [FAQ oficial](https://anthropic-partners.skilljar.com/page/faq-certifications). O uso destas skills para estudar é independente da inscrição no exame.

As questões são próprias de estudo. A skill combina itens do banco por domínio com questões geradas para preencher as vagas restantes, identificando a origem, o estado de revisão e eventuais repetições. Nenhuma questão é oficial. Os resultados indicam desempenho observado e não preveem aprovação. As skills não devem ser usadas para responder uma prova oficial em andamento ou acessar questões vazadas. Referências devem ser verificadas quando houver acesso à internet; sem consulta, sua pertinência deve ser sinalizada como não verificada.

O banco piloto da Developer contém cinco questões em quatro domínios, com revisão documental assistida por IA e sem validação independente de especialista. Os outros bancos ainda estão vazios. A geração complementa as cotas que não forem preenchidas pelo banco. A preferência inicial é usar cerca de metade das vagas por domínio do banco, quando houver itens suficientes; não se trata de proporção oficial.

Depois da correção, erros e acertos com confiança baixa entram numa fila de revisão. Após estudar o conceito, o tutor pergunta “Pronto para tentar de novo?”. O resultado original permanece preservado. Muitos itens com confiança 1 pedem estudo dirigido, mesmo quando corretos; erros com confiança 3 pedem revisão prioritária do critério de decisão. O progresso pode ser salvo pelo agente em arquivo da sessão, quando o ambiente permitir, ou exportado manualmente.

## Conteúdo e atualização

Os domínios e pesos refletem a base de 10/11/2026 e não foram integralmente verificados contra os guias oficiais autenticados. Consulte o guia oficial aplicável antes de se preparar ou agendar uma prova. `references/fontes.md` em cada skill registra as fontes disponíveis.

## Ferramentas

`tools/build_skills.py` regenera as skills e os ZIPs a partir de `tools/baseline.json` e dos recursos compartilhados. Requer Python 3.9 ou superior e usa a biblioteca padrão:

```bash
python tools/build_skills.py
```

Cada skill inclui uma cópia independente de `scripts/avaliar.py`; a execução Python é opcional. Sem ela, o agente pode calcular os resultados manualmente seguindo a metodologia da skill.

`scripts/montar_avaliacao.py --mode quick` (ou `deep`/`full`) cria um plano de questões do banco e vagas para geração, sem imprimir gabaritos. Dentro de cada skill, `references/banco-revisao.md` explica a seleção, a fila de revisão e a leitura dos padrões de confiança. Respostas pessoais devem ficar fora das pastas das skills e não devem ser incorporadas ao banco público.
