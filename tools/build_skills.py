#!/usr/bin/env python3
"""Gera quatro skills independentes e auditáveis de uma versão-fonte preservada."""
from __future__ import annotations
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from montar_avaliacao import validate_bank

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / 'tools' / 'baseline.json'
OUT = ROOT / 'skills'
ZIPS = ROOT / 'packages'
VERSION = '1.1.1'

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
         quick=[5,2,2,2,2,1,1,1], deep=[11,5,5,3,3,3,1,1],
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

Na primeira interação, usar a apresentação salva para informar o contexto do programa para organizações parceiras e orientar a conferir elegibilidade antes da inscrição. Não consultar o portal automaticamente para iniciar o estudo. O uso desta skill é independente e não exige informar empresa ou e-mail. Fonte de referência: https://anthropic-partners.skilljar.com/page/faq-certifications .

## Antes de responder

1. Ao escolher esta certificação, ler `references/inicio.md` e usar a apresentação salva. Não ler outras skills, regenerar um mapa ou pesquisar atualizações para reproduzir esse conteúdo versionado; consultar fontes atuais somente se necessário para uma dúvida, divergência concreta ou pedido de atualização.
2. Carregar apenas os materiais necessários ao pedido: `references/escopo-base.md` e `references/dominios.json` para detalhes de cobertura; `references/metodologia.md` para conduzir estudo ou avaliação.
3. Ler `references/banco-revisao.md` antes de montar avaliações e revisar erros, `references/qualidade-questoes.md` antes de criar questões ou correções e `references/avaliacao.md` ao calcular resultados ou retomar progresso. Os exercícios sugeridos em `references/laboratorios.md` são atividades de raciocínio respondidas na conversa; não exigem criar arquivos ou executar programas.
4. Se houver novo guia oficial, **sinalizar sua existência e divergências** sem substituir automaticamente os conteúdos desta versão. Uma atualização de syllabus requer nova revisão e versão da skill.

## Ativação e modos

- **Local da experiência:** ensinar e aplicar todas as questões nesta conversa. Não criar simulador, programa Python, aplicação, interface ou laboratório executável por iniciativa própria. Os scripts já incluídos podem auxiliar o tutor internamente a calcular ou selecionar itens; não são a experiência do estudante. Só criar ou executar um exercício de programação se o estudante pedir explicitamente esse tipo de atividade.
- **Diagnóstico:** rápido com {quick_n} questões (`{quick_repr}`) ou aprofundado com {deep_n} (`{deep_repr}`). Cobrir todos os domínios; as amostras pequenas são apenas indicativas.
- **Estudar:** consultar o conteúdo salvo, explicar o trecho pertinente aqui, apresentar exemplo e pergunta de verificação e corrigir após resposta. Um pedido de conteúdo completo deve reutilizar material existente, sem escrever nova apostila ou arquivo a cada sessão.
- **Praticar:** questões situacionais inéditas, em inglês, uma por vez, com feedback após tentativa.
- **Simulado completo:** **{q} questões / 120 minutos** segundo a versão-fonte, uma por vez, incluindo múltipla resposta; corrigir somente no final. Não fingir cronômetro automático.
- **Revisar/progresso:** manter fila de erros e acertos inseguros, estudar o conceito e perguntar “Pronto para tentar de novo?”. Registrar novas tentativas, confiança e progresso sem sobrescrever a avaliação anterior.
- **Planejar:** construir cronograma realista a partir de tempo disponível, objetivos e erros observados; nunca inventar compromissos de agenda.

Se o usuário pedir um modo diretamente, começar esse modo sem impor menu. Quando apenas escolher {code} ou pedir preparação genérica, apresentar domínios e recursos relevantes e perguntar se deseja um diagnóstico, aguardando resposta. Antes da primeira questão do diagnóstico, perguntar a disponibilidade semanal e eventual data-alvo, aceitando que não saiba ou não queira informar. Aproveitar dados já fornecidos e usá-los após a correção; não voltar a perguntar ao final.

## Regras específicas desta prova

{focus}

- Idioma da explicação: português brasileiro; enunciado de questões e nomes de recursos/domínios em inglês.
- Antes de fazer questão, assegurar que há resposta **defensável**, distratores plausíveis e **quatro** alternativas. Distribuir escolha simples e 'Choose TWO' segundo a metodologia, sem alternância previsível; as proporções são pedagógicas.
- Combinar itens de `assets/banco-questoes.json` com questões geradas nas vagas restantes, preservando cotas por domínio. Identificar a origem e o estado real de revisão e sinalizar repetições. Nenhum item é oficial. Usar `python scripts/montar_avaliacao.py --mode quick` (ou `deep`/`full`) quando possível; sem execução, seguir `references/banco-revisao.md` manualmente.
- Durante diagnóstico e simulado: **não revelar acertos, erros, dicas ou gabarito**, nem mesmo por elogios. Solicitar resposta (letra(s)) e confiança 1–3, registrar e seguir.
- Preservar itens anulados com motivo, excluí-los das contas e recompor cobertura quando necessário; seguir `references/avaliacao.md`.
- Separar percentual bruto de acertos, calibração de confiança e cobertura. Não misturar pontos de confiança com porcentagem de acertos. Um domínio com uma questão não é considerado dominado.
- Destacar padrões de confiança: vários itens com 1, mesmo corretos, pedem estudo e justificativa; erros com 3 pedem revisão prioritária do conceito. Usar a fila de revisão e oferecer nova tentativa após o estudo, sem exigir confiança alta artificialmente.
- **720/1000 é escala da prova, não conversão de acertos:** nunca estimar nota escalonada ou probabilidade de aprovação a partir de questões geradas.
- Resolver comandos e referências a partir da pasta real desta skill. Para computação determinística, se houver execução Python: `python scripts/avaliar.py --allocate` e `python scripts/avaliar.py --input respostas.json`. Caso contrário, calcular manualmente segundo `references/metodologia.md`. Não declarar script executado sem execução.
- Laboratórios usam casos fictícios. Nunca solicitar chave de API, dados de cliente ou credenciais de trabalho.

## Material e atualização

- `references/escopo-base.md`: domínios, pesos, tópicos e fatos **transcritos da fonte**; as tabelas não equivalem a validação de todos os itens pelo portal oficial.
- `references/inicio.md`: apresentação pronta, domínios e recursos de estudo. Usar diretamente ao selecionar a certificação.
- `references/fontes.md`: fontes declaradas pelo documento original e hash da base; não são comprovação de consulta aos guias oficiais.
- `references/laboratorios.md`: atividades recomendadas que **não ampliam o syllabus**.
- `references/ingles-cenarios.md`: vocabulário de negócio, interpretação de públicos/objetivos e casos guiados. Consultar no estudo e na correção de dúvidas de leitura; não antecipar dicas durante diagnóstico/simulado.
- `references/banco-revisao.md`: montagem híbrida, procedência das questões, confiança e fila de revisão. O banco inclui gabaritos para uso do tutor; não exibi-los durante a aplicação.
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
        minimum = 1 if cfg['code'] == 'CCDV-F' else 3
        if any(type(n) is not int or n < minimum for n in cfg['deep']):
            raise RuntimeError('Diagnóstico aprofundado não cobre todos os domínios')


def write(p, content):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('w', encoding='utf-8', newline='\n') as stream:
        stream.write(content)


def introduction(cfg, domains):
    rows = '\n'.join(f'| {d["name"]} | {d["weight_percent"]:g}% | {d["topics"]} |' for d in domains)
    materials = ('- [Conteúdo de estudo salvo](guia-estudo.md): explicações, exemplos e exercícios por domínio.\n'
                 '- [Roteiro e leituras por assunto](roteiro-estudo.md).\n'
                 '- [Vídeos de apoio da Anthropic](videos-estudo.md): seleção por assunto e perguntas para revisar depois.\n'
                 '- [Trilha Claude Developer](https://anthropic-partners.skilljar.com/path/claude-developer).\n'
                 '- [Preparação Developer Foundations](https://anthropic-partners.skilljar.com/path/claude-certified-developer-foundations).'
                 if cfg['code'] == 'CCDV-F' else
                 '- [Escopo por domínio](escopo-base.md).\n- [Fontes de referência](fontes.md).\n'
                 '- [Certificações e preparação na Partner Academy](https://anthropic-partners.skilljar.com/page/partner-certifications).')
    materials += '\n- [Inglês dos cenários](ingles-cenarios.md): públicos, vocabulário de negócio, objetivos e restrições.'
    return (f'# {cfg["title"]} ({cfg["code"]})\n\n'
            'Esta certificação integra o programa da Anthropic para organizações parceiras. Confirme elegibilidade e acesso na [FAQ oficial](https://anthropic-partners.skilljar.com/page/faq-certifications); estudar com esta skill não exige informar empresa ou e-mail.\n\n'
            '## Conteúdo desta preparação\n\nBase de conteúdo: 10/11/2026. Os domínios e pesos abaixo são os da baseline, ainda não integralmente conferida com o guia oficial autenticado.\n\n'
            '| Domínio | Peso | Assuntos |\n|---|---:|---|\n'+rows+'\n\n'
            '## Materiais para estudar\n\n'+materials+'\n\n'
            'Os links fazem parte do material salvo; sua presença não significa que foram consultados nesta sessão. Os cursos da Partner Academy podem exigir acesso autorizado.\n\n'
            'Vamos estudar e responder questões aqui na conversa. As questões são próprias de estudo, com origem identificada; não são itens oficiais. A pontuação escalonada oficial não pode ser convertida diretamente em percentual de acertos.\n\n'
            '**Gostaria de fazer um teste para medir seu conhecimento atual?**\n'
            f'Opções: {sum(cfg["quick"])} questões, {sum(cfg["deep"])} questões ou simulado de {cfg["q"]}, conforme a baseline. Antes de começar, vamos considerar sua disponibilidade semanal e eventual data-alvo.\n')


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
        bank_path = ROOT/'tools'/('banco-ccdv.json' if cfg['code'] == 'CCDV-F' else 'banco-'+cfg['code'].lower()+'.json')
        bank = json.loads(bank_path.read_text(encoding='utf-8')) if bank_path.exists() else dict(
            schema_version='1.0', exam_code=cfg['code'], baseline='2026-11-10',
            review_scope='Banco ainda sem itens; gerar questões seguindo o padrão de qualidade.', domains={})
        validate_bank(manifest, bank)
        write(skill/'assets'/'banco-questoes.json', json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
        write(skill/'references'/'dominios.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
        write(skill/'references'/'inicio.md', introduction(cfg, domains))
        write(skill/'references'/'escopo-base.md',baseline[cfg['code']]['scope'])
        write(skill/'references'/'metodologia.md', METHOD)
        write(skill/'references'/'qualidade-questoes.md',QUALITY)
        write(skill/'references'/'avaliacao.md',ASSESSMENT)
        write(skill/'references'/'banco-revisao.md', (ROOT/'tools'/'banco-revisao.md').read_text(encoding='utf-8'))
        write(skill/'references'/'ingles-cenarios.md', (ROOT/'tools'/'ingles-cenarios.md').read_text(encoding='utf-8'))
        if cfg['code'] == 'CCDV-F':
            write(skill/'references'/'roteiro-estudo.md', (ROOT/'tools'/'roteiro-ccdv.md').read_text(encoding='utf-8'))
            write(skill/'references'/'guia-estudo.md', (ROOT/'tools'/'guia-ccdv.md').read_text(encoding='utf-8'))
            write(skill/'references'/'videos-estudo.md', (ROOT/'tools'/'videos-ccdv.md').read_text(encoding='utf-8'))
        write(skill/'references'/'fontes.md',baseline[cfg['code']]['sources'])
        exercises='\n\n'.join(f'### {topic}\n\n{body}' for topic,body in cfg['exercises'])
        write(skill/'references'/'laboratorios.md',f'# Exercícios sugeridos para {cfg["code"]}\n\n**Atenção:** são exercícios pedagógicos gerados para esta skill, não exigências adicionais confirmadas pelo guia oficial. Usar apenas o escopo e domínios de `escopo-base.md`. Resolver na conversa, com explicação, texto ou pseudocódigo; só criar arquivos ou executar código se o estudante pedir explicitamente uma atividade de programação.\n\n{exercises}\n\n## Como avaliar\n\nPara cada atividade: estabelecer critério de aceite simples, pedir primeiro a decisão do estudante, apontar trade-off omitido, propor correção e registrar tópico que precisa de revisão.\n')
        write(skill/'assets'/'progresso-template.json', json.dumps(dict(schema_version='1.2',exam_code=cfg['code'],skill_version=VERSION,source_baseline='2026-11-10',session_date=None,study_goal=None,planned_exam_date=None,study_schedule=dict(days_per_week=[],hours_per_day=None),profile=dict(experience=None,english=None,learning_style=None),evaluations=[],active_assessment=None,topic_history=[],review_queue=[],domains={d['id']:dict(name=d['name'],questions_answered=0,correct=0,accuracy_percent=None,false_certainty_count=0,error_topics=[],notes=[]) for d in domains},next_actions=[],notes=['Preencher com resultados observados; não é boletim oficial.']),ensure_ascii=False,indent=2)+'\n')
        write(skill/'assets'/'relatorio-template.md',f'# Relatório portável de estudo — {cfg["code"]}\n\n- Versão da skill: v{VERSION}; escopo-fonte: 10/11/2026\n- Data da sessão: [preencher]\n- Objetivo e data da prova, se houver: [preencher]\n- Modalidade: [diagnóstico rápido / aprofundado / simulado / prática]\n- Amostra: [N] questões de [N] domínios; cobertura dos subtópicos: [informar]\n\n| Domínio | Peso da fonte | Questões | Acertos | Acerto bruto | Falsa certeza | Lacunas |\n|---|---:|---:|---:|---:|---:|---|\n| [preencher] | | | | | | |\n\n**Confiança e revisão:** [N] respostas com confiança 1; [N] acertos com dúvida; [N] erros com confiança 3. [Tópicos e próxima tentativa após estudo.]\n\n**Limitações:** simulado original gerado por IA, resultado não é nota oficial escalonada nem previsão de aprovação.\n\n**Padrões de erro:** [preencher]\n\n**3–5 tópicos prioritários e exercícios:** [preencher]\n\n**Plano e próximos checkpoints:** [preencher]\n\n**Transferência:** copie este relatório para a nova conversa. Não incluir dados de cliente, chaves ou credenciais.\n')
        shutil.copy2(ROOT/'tools'/'avaliar.py',skill/'scripts'/'avaliar.py')
        shutil.copy2(ROOT/'tools'/'montar_avaliacao.py',skill/'scripts'/'montar_avaliacao.py')
        quick_repr=', '.join(f'D{i+1}:{v}' for i,v in enumerate(cfg['quick']))
        deep_repr=', '.join(f'D{i+1}:{v}' for i,v in enumerate(cfg['deep']))
        desc=f'Preparação para {cfg["code"]}: diagnóstico por domínios, prática, simulados e plano de estudo. Usar para dúvidas, revisão ou treinamento dessa certificação Claude.'
        if len(desc)>200:
            raise RuntimeError(f'Descrição excede 200 chars Claude Help: {len(desc)} {cfg["code"]}')
        skill_md=SKILL_TEMPLATE.format(version=VERSION,name=cfg['name'],code=cfg['code'],title=cfg['title'],trigger=cfg['trigger'],
                             focus=FOCUS[cfg['code']],quick_n=sum(cfg['quick']),deep_n=sum(cfg['deep']),
                             quick_repr=quick_repr,deep_repr=deep_repr,q=cfg['q'])
        if cfg['code'] == 'CCDV-F':
            skill_md += ('\n**Conteúdo de estudo pronto:** `references/guia-estudo.md` contém a teoria dos oito domínios, exemplos e exercícios. '
                         'Se pedir “conteúdo completo”, disponibilizar o guia já existente e seu índice; oferecer os capítulos aqui, sem recriar o documento. '
                         'Para assunto específico, localizar e ler somente a seção relevante. Não pesquisar a web nem escrever arquivos para apenas recuperar este material salvo; '
                         'pesquisar somente quando houver dúvida técnica não coberta, necessidade de verificar um detalhe variável ou pedido explícito. '
                         'Consultar `references/roteiro-estudo.md` para as leituras por lacuna.\n')
        write(skill/'SKILL.md',skill_md)
        create_zip(skill,ZIPS/(cfg['name']+'.zip'))
    # zip consolidado para arquivamento / manutenção, não upload direto de skill
    with zipfile.ZipFile(ROOT.parent/f'claude-certification-skills-v{VERSION}-completo.zip','w',zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(ROOT.rglob('*')):
            relative = p.relative_to(ROOT)
            if (p.is_file() and '__pycache__' not in p.parts and
                    (relative.parts[0] in ('skills', 'tools', 'packages') or
                     relative.as_posix() in ('README.md', '.gitignore', '.gitattributes'))):
                z.write(p,arcname=p.relative_to(ROOT.parent).as_posix())
    print('Geradas 4 skills a partir da baseline versionada')
    for cfg in CONFIG:
        print(cfg['code'],cfg['name'],sum(cfg['quick']),sum(cfg['deep']), (ZIPS/(cfg['name']+'.zip')).stat().st_size)

if __name__=='__main__':
    main()
