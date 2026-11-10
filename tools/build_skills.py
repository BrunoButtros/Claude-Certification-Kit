#!/usr/bin/env python3
"""Gera quatro skills independentes e auditáveis de uma versão-fonte preservada."""
from __future__ import annotations
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / 'tools' / 'baseline.json'
OUT = ROOT / 'skills'
ZIPS = ROOT / 'packages'
VERSION = '1.0.1'

CONFIG = [
    dict(code='CCAO-F', name='ccao-foundations-study', title='Claude Certified Associate – Foundations', q=60,
         quick=[2,3,2,2,2,2,1], deep=[4,6,3,4,3,5,3],
         trigger='Associate Foundations, CCAO-F, prova de produtividade com Claude',
         exercises=[
             ('Avaliação de saída', 'Comparar duas respostas sobre uma política fictícia; classificar precisão, completude, viés e necessidades de revisão humana.'),
             ('Seleção de produto', 'Escolher entre Chat, Projects, Research e Artifacts para três tarefas de trabalho com restrições de contexto.'),
             ('Governança', 'Reescrever um fluxo de negócio para remover dados pessoais desnecessários e acrescentar pontos de aprovação humana.'),
             ('Troubleshooting', 'Diagnosticar uma resposta insatisfatória distinguindo prompt vago, contexto ausente e fonte inadequada.'),
         ]),
    dict(code='CCDV-F', name='ccdv-foundations-study', title='Claude Certified Developer – Foundations', q=53,
         quick=[5,2,2,2,2,1,1,1], deep=[11,6,6,4,4,3,3,3],
         trigger='Developer Foundations, CCDV-F, certificação de API e integração',
         exercises=[
             ('Messages API', 'Raciocinar sobre roles, system, stop_reason e fluxo de retorno; usar payload fictício sem credenciais reais.'),
             ('Confiabilidade', 'Projetar tratamento de 429/529, backoff e idempotência para uma chamada de API sob falhas.'),
             ('Tools e MCP', 'Definir um JSON Schema mínimo para ferramenta e planejar tratamento de tool_result e is_error.'),
             ('Evals e segurança', 'Criar cinco casos de avaliação e um teste de prompt injection para uma integração simulada.'),
         ]),
    dict(code='CCAR-F', name='ccar-foundations-study', title='Claude Certified Architect – Foundations', q=60,
         quick=[3,3,2,2,2], deep=[7,5,5,4,4],
         trigger='Architect Foundations, CCAR-F, arquitetura de agentes e Claude Code',
         exercises=[
             ('Orquestração', 'Desenhar agente coordenador e dois especialistas com escopos explícitos, falhas esperadas e passagem de contexto.'),
             ('Controles determinísticos', 'Decidir se uma regra deve ser assegurada por hook, permissão, validação de código ou instrução textual.'),
             ('MCP e ferramentas', 'Revisar uma coleção de tools e identificar descrições ambíguas, excesso de privilégio e tratamento de erros.'),
             ('Confiabilidade', 'Projetar compactação, rastreabilidade de fontes e recuperação de falhas num workflow multiagente.'),
         ]),
    dict(code='CCAR-P', name='ccar-professional-study', title='Claude Certified Architect – Professional', q=63,
         quick=[2,2,2,2,2,2,1], deep=[5,3,5,4,4,4,3],
         trigger='Architect Professional, CCAR-P, arquitetura corporativa e governança',
         exercises=[
             ('Decisão de arquitetura', 'Escrever um ADR curto comparando workflow, agente e multiagente sob orçamento, SLA e requisito regulatório fictícios.'),
             ('Avaliação e observabilidade', 'Projetar conjunto de métricas para precisão, segurança, custo, latência, disponibilidade e qualidade operacional.'),
             ('Segurança e governança', 'Criar matriz de responsabilidades de aprovação humana para ferramentas de baixo e alto impacto.'),
             ('Stakeholders', 'Explicar trade-offs técnicos para um diretor não técnico e definir métricas de aceite e ciclo de feedback.'),
         ]),
]

# Textos canônicos mantidos fora do gerador para evitar sobrescrever revisões.
METHOD = (ROOT / 'tools' / 'metodologia.md').read_text(encoding='utf-8')
QUALITY = (ROOT / 'tools' / 'qualidade-questoes.md').read_text(encoding='utf-8')
ASSESSMENT = (ROOT / 'tools' / 'avaliacao.md').read_text(encoding='utf-8')

SKILL_TEMPLATE = '''---
name: {name}
description: "Preparação para {code}: diagnóstico por domínios, prática, simulados e plano de estudo. Usar para dúvidas, revisão ou treinamento dessa certificação Claude."
metadata:
  version: "{version}"
  exam: "{code}"
  source_baseline: "2026-11-10"
---

# Tutor de certificação — {title} ({code})

**Objetivo:** orientar aprendizagem, avaliar lacunas e planejar revisão para **{code}**, sem ajudar durante prova oficial. O conteúdo examinável desta entrega está **congelado na versão-fonte de 10/11/2026**. Nunca trocar os pesos ou incluir novo conteúdo oficial silenciosamente.

## Antes de responder

1. Abrir `references/escopo-base.md` e `references/dominios.json` para identificar domínios, pesos e tópicos.
2. Ler `references/metodologia.md` na primeira ativação para adotar os modos de estudo, diagnóstico, apuração, segurança e planejamento.
3. Ler `references/qualidade-questoes.md` antes de criar questões ou correções, `references/avaliacao.md` ao calcular resultados ou retomar progresso, e `references/laboratorios.md` quando propor atividade prática.
4. Se houver novo guia oficial, **sinalizar sua existência e divergências** sem substituir automaticamente os conteúdos desta versão. Uma atualização de syllabus requer nova revisão e versão da skill.

## Ativação e modos

- **Diagnóstico:** rápido com {quick_n} questões (`{quick_repr}`) ou aprofundado com {deep_n} (`{deep_repr}`). Cobrir todos os domínios; as amostras pequenas são apenas indicativas.
- **Estudar:** explicar conceitos do domínio desejado, apresentar exemplo prático, pergunta de verificação e corrigir após resposta.
- **Praticar:** questões situacionais inéditas, em inglês, uma por vez, com feedback após tentativa.
- **Simulado completo:** **{q} questões / 120 minutos** segundo a versão-fonte, uma por vez, incluindo múltipla resposta; corrigir somente no final. Não fingir cronômetro automático.
- **Revisar/progresso:** comparar desempenho com cobertura e versão do guia, fazer revisão de erros e exportar resumo portável.
- **Planejar:** construir cronograma realista a partir de tempo disponível, objetivos e erros observados; nunca inventar compromissos de agenda.

Se o usuário pedir um modo diretamente, **começar esse modo** sem oferecer menu. Para pedido genérico de ajuda para {code}, oferecer escolha breve entre diagnóstico rápido, estudar, praticar ou simulado; por padrão iniciar diagnóstico rápido se disser apenas 'começar'. Solicitar só informações imprescindíveis e não repetir dados já informados.

## Regras específicas desta prova

{focus}

- Idioma da explicação: português brasileiro; enunciado de questões e nomes de recursos/domínios em inglês.
- Antes de fazer questão, assegurar que há resposta **defensável**, distratores plausíveis e **quatro** alternativas. Distribuir escolha simples e 'Choose TWO' segundo a metodologia, sem alternância previsível; as proporções são pedagógicas.
- Durante diagnóstico e simulado: **não revelar acertos, erros, dicas ou gabarito**, nem mesmo por elogios. Solicitar resposta (letra(s)) e confiança 1–3, registrar e seguir.
- Preservar itens anulados com motivo, excluí-los das contas e recompor cobertura quando necessário; seguir `references/avaliacao.md`.
- Separar percentual bruto de acertos, calibração de confiança e cobertura. Não misturar pontos de confiança com porcentagem de acertos. Um domínio com uma questão não é considerado dominado.
- **720/1000 é escala da prova, não conversão de acertos:** nunca estimar nota escalonada ou probabilidade de aprovação a partir de questões geradas.
- Resolver comandos e referências a partir da pasta real desta skill. Para computação determinística, se houver execução Python: `python scripts/avaliar.py --allocate` e `python scripts/avaliar.py --input respostas.json`. Caso contrário, calcular manualmente segundo `references/metodologia.md`. Não declarar script executado sem execução.
- Laboratórios usam casos fictícios. Nunca solicitar chave de API, dados de cliente ou credenciais de trabalho.

## Material e atualização

- `references/escopo-base.md`: domínios, pesos, tópicos e fatos **transcritos da fonte**; as tabelas não equivalem a validação de todos os itens pelo portal oficial.
- `references/fontes.md`: fontes declaradas pelo documento original e hash da base; não são comprovação de consulta aos guias oficiais.
- `references/laboratorios.md`: atividades recomendadas que **não ampliam o syllabus**.
- `assets/progresso-template.json` e `assets/relatorio-template.md`: persistência manual e relatório para novas conversas; validar certificação/base/versão e preservar histórico conforme `references/avaliacao.md`.
- Guias e cursos: https://anthropic-partners.skilljar.com/page/partner-certifications ; https://anthropic-partners.skilljar.com/page/claude-certification-exam-prep-courses ; https://www.pearsonvue.com/us/en/anthropic.html . Não inventar páginas de documentação específicas.

**Importante:** estas skills são materiais independentes de estudo; não há ligação com plataforma, relógio ou calendário por padrão. Nenhuma notificação/reavaliação é executada em segundo plano.
'''

FOCUS = {
    'CCAO-F': '- Foco educacional: distinguir qualidade de resposta, adequação ao contexto, escolha de recursos, governança e recuperação de um workflow; exercícios sem exigir código ou API.',
    'CCDV-F': '- Foco educacional: domínios de API e integração (33,1% na fonte), tratamento de erros, caching, batches, agent loops, tools/MCP, segurança e evals. Cobrir os oito domínios inclusive Claude Code e Evaluation, Testing & Debugging.',
    'CCAR-F': '- Foco educacional: decisões de arquitetura de sistemas agentic, Claude Code, ferramentas/MCP, structured output e confiabilidade. Questões devem ter restrições que diferenciem soluções apenas possíveis da melhor solução de produção.',
    'CCAR-P': '- Foco educacional: arquitetura ponta a ponta, integração empresarial, avaliação, governança, stakeholders e enablement. Questões corporativas devem explicitar restrições de negócio, risco, tempo e custo.',
}


def validate_config(baseline):
    if len(CONFIG) != 4 or set(baseline) != {c['code'] for c in CONFIG}:
        raise RuntimeError('Esperava quatro configurações independentes')
    for cfg in CONFIG:
        domains = baseline[cfg['code']]['domains']
        if (not domains or len({d['id'] for d in domains}) != len(domains)
                or any(not 0 < d['weight_percent'] <= 100 for d in domains)
                or abs(sum(d['weight_percent'] for d in domains) - 100) > 0.01):
            raise RuntimeError('Domínios ou pesos inválidos')
        if not len(domains) == len(cfg['quick']) == len(cfg['deep']):
            raise RuntimeError('Distribuição incompatível: ' + cfg['code'])
        if any(type(n) is not int or n < 1 for n in cfg['quick']):
            raise RuntimeError('Diagnóstico rápido deve cobrir todos os domínios')
        if any(type(n) is not int or n < 3 for n in cfg['deep']):
            raise RuntimeError('Diagnóstico aprofundado exige três itens por domínio')


def write(p, content):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8', newline='\n') as stream:
        stream.write(content)


def create_zip(source_dir, output):
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(source_dir.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                z.write(p,arcname=p.relative_to(source_dir.parent).as_posix())


def main():
    baseline=json.loads(BASELINE.read_text(encoding='utf-8'))
    validate_config(baseline)
    OUT.mkdir(parents=True,exist_ok=True)
    ZIPS.mkdir(parents=True,exist_ok=True)
    for cfg in CONFIG:
        domains=baseline[cfg['code']]['domains']
        skill=OUT/cfg['name']
        (skill/'references').mkdir(parents=True,exist_ok=True)
        (skill/'assets').mkdir(exist_ok=True)
        (skill/'scripts').mkdir(exist_ok=True)
        manifest=dict(exam_code=cfg['code'],exam_title=cfg['title'],exam_questions=cfg['q'],duration_minutes=120,source_baseline='2026-11-10', version=VERSION,
                      quick_distribution={d['id']:cfg['quick'][i] for i,d in enumerate(domains)},
                      deep_distribution={d['id']:cfg['deep'][i] for i,d in enumerate(domains)},
                      domains=domains)
        if not sum(cfg['deep']) > sum(cfg['quick']) > 0:
            raise RuntimeError('Totais de diagnóstico incompatíveis')
        write(skill/'references'/'dominios.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        write(skill/'references'/'escopo-base.md',baseline[cfg['code']]['scope'])
        write(skill/'references'/'metodologia.md', METHOD)
        write(skill/'references'/'qualidade-questoes.md',QUALITY)
        write(skill/'references'/'avaliacao.md',ASSESSMENT)
        write(skill/'references'/'fontes.md',baseline[cfg['code']]['sources'])
        exercises='\n\n'.join(f'### {topic}\n\n{body}' for topic,body in cfg['exercises'])
        write(skill/'references'/'laboratorios.md',f'# Exercícios sugeridos para {cfg["code"]}\n\n**Atenção:** são exercícios pedagógicos gerados para esta skill, não exigências adicionais confirmadas pelo guia oficial. Usar apenas o escopo e domínios de `escopo-base.md`.\n\n{exercises}\n\n## Como avaliar\n\nPara cada atividade: estabelecer critério de aceite simples, pedir primeiro a decisão do estudante, apontar trade-off omitido, propor correção e registrar tópico que precisa de revisão.\n')
        write(skill/'assets'/'progresso-template.json', json.dumps(dict(schema_version='1.1',exam_code=cfg['code'],skill_version=VERSION,source_baseline='2026-11-10',session_date=None,study_goal=None,planned_exam_date=None,study_schedule=dict(days_per_week=[],hours_per_day=None),profile=dict(experience=None,english=None,learning_style=None),evaluations=[],active_assessment=None,topic_history=[],domains={d['id']:dict(name=d['name'],questions_answered=0,correct=0,accuracy_percent=None,false_certainty_count=0,error_topics=[],notes=[]) for d in domains},next_actions=[],notes=['Preencher com resultados observados; não é boletim oficial.']),ensure_ascii=False,indent=2)+'\n')
        write(skill/'assets'/'relatorio-template.md',f'# Relatório portável de estudo — {cfg["code"]}\n\n- Versão da skill: v{VERSION}; escopo-fonte: 10/11/2026\n- Data da sessão: [preencher]\n- Objetivo e data da prova, se houver: [preencher]\n- Modalidade: [diagnóstico rápido / aprofundado / simulado / prática]\n- Amostra: [N] questões de [N] domínios; cobertura dos subtópicos: [informar]\n\n| Domínio | Peso da fonte | Questões | Acertos | Acerto bruto | Falsa certeza | Lacunas |\n|---|---:|---:|---:|---:|---:|---|\n| [preencher] | | | | | | |\n\n**Limitações:** simulado original gerado por IA, resultado não é nota oficial escalonada nem previsão de aprovação.\n\n**Padrões de erro:** [preencher]\n\n**3–5 tópicos prioritários e exercícios:** [preencher]\n\n**Plano e próximos checkpoints:** [preencher]\n\n**Transferência:** copie este relatório para a nova conversa. Não incluir dados de cliente, chaves ou credenciais.\n')
        shutil.copy2(ROOT/'tools'/'avaliar.py',skill/'scripts'/'avaliar.py')
        quick_repr=', '.join(f'D{i+1}:{v}' for i,v in enumerate(cfg['quick']))
        deep_repr=', '.join(f'D{i+1}:{v}' for i,v in enumerate(cfg['deep']))
        desc=f'Preparação para {cfg["code"]}: diagnóstico por domínios, prática, simulados e plano de estudo. Usar para dúvidas, revisão ou treinamento dessa certificação Claude.'
        if len(desc)>200:
            raise RuntimeError(f'Descrição excede 200 chars Claude Help: {len(desc)} {cfg["code"]}')
        skill_md=SKILL_TEMPLATE.format(version=VERSION,name=cfg['name'],code=cfg['code'],title=cfg['title'],trigger=cfg['trigger'],
                             focus=FOCUS[cfg['code']],quick_n=sum(cfg['quick']),deep_n=sum(cfg['deep']),
                             quick_repr=quick_repr,deep_repr=deep_repr,q=cfg['q'])
        write(skill/'SKILL.md',skill_md)
        create_zip(skill,ZIPS/(cfg['name']+'.zip'))
    # zip consolidado para arquivamento / manutenção, não upload direto de skill
    with zipfile.ZipFile(ROOT.parent/f'claude-certification-skills-v{VERSION}-completo.zip','w',zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(ROOT.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:
                z.write(p,arcname=p.relative_to(ROOT.parent).as_posix())
    print('Geradas 4 skills a partir da baseline versionada')
    for cfg in CONFIG:
        print(cfg['code'],cfg['name'],sum(cfg['quick']),sum(cfg['deep']), (ZIPS/(cfg['name']+'.zip')).stat().st_size)

if __name__=='__main__':
    main()
