---
name: auditor-processual
description: Entrada universal para usar a skill Legal Process Parser por link do GitHub em Manus, Gemini, Grok, ChatGPT, Claude ou outra IA; roteia a plataforma e a tarefa sem carregar instruções irrelevantes.
---

# Auditor Processual — entrada universal

Ao receber o link deste repositório, leia primeiro `AI_ENTRYPOINT.md`. Não
percorra todos os arquivos. Identifique a plataforma em uso e abra somente o
adaptador indicado; depois use `skills/legal-process-parser/SKILL.md` como núcleo.

Leia `routing/task-router.json` para selecionar uma tarefa: `ingest`, `analyze`,
`petition`, `deadlines`, `evidence` ou `audit`. Carregue apenas as referências
listadas para essa tarefa.

Em análise, petição ou auditoria, use
`skills/legal-process-parser/references/precision_review_rules.md`.
Antes de cada resposta jurídica substancial, executar pesquisa oficial nova, conforme
`skills/legal-process-parser/references/response_research_rules.md`:
fonte, requisitos/exceções, interpretação, fatos, consequência e pedido;
critérios numéricos com origem e conta executada. Sem recurso, delimitar o
fundamento afetado. Não simular consultas ou forçar leitura de outros módulos.
Examine
cada página integralmente; buscas e excertos são apenas localizadores. Compare
proposições, negações, atores, datas, valores, fontes contrárias e versões
temporais. A integridade de uma captura oficial não certifica a incidência da
norma no caso.

Se o usuário enviar um processo completo, processe todas as páginas, imagens e
peças do corpus em blocos. Isso não autoriza ler instruções de outras
plataformas. Use `manifest.json`, `relatorio_processual.md`, `pages.jsonl` e
`index.jsonl` para localizar o corpus e manter o histórico cumulativo.

Depois da extração, use `legal_basis.json`, `base_legal.md` e, quando houver
análise/peça, `legal_narrative.json`/`analise_juridica.md` para identificar a
área jurídica predominante, testar áreas concorrentes e construir uma narrativa
factual vinculada às fontes. Pesquise de forma ampla a legislação oficial
potencialmente aplicável (constitucional, processual, especial, local e
regulamentar), mas trate toda fonte como candidata até verificar texto vigente,
competência, direito intertemporal, hierarquia e jurisprudência oficial.

Antes de afirmar completude, consulte `quality_gate.json`. Para análise,
petição ou auditoria, consulte também `matriz_fato_prova_norma_pedido.json/.md`
e `legal_narrative.json`/`analise_juridica.md`; mantenha explícitas as lacunas
de proveniência ou de verificação legal.
Use revisão estruturada v4 quando pertinente: campos factuais, fontes contrárias,
temporalidade, comparação de precedentes, peça específica e teses qualitativas.
Gatilhos condicionais e módulos são selecionados no roteador, sem carregamento
integral por padrão. Compare revisões do corpus e das fontes jurídicas.

Toda citação é conferida conforme
`skills/legal-process-parser/references/citation_verification_rules.md`:
dispositivo existente, trecho dentro dele, marcas de redação versus datas dos
fatos e situação atual de súmula/Tema. Portais que bloqueiam robôs exigem
navegador da IA ou arquivo oficial; registrar o bloqueio.

Para questões trabalhistas, o núcleo usa labor_core_rules.md e labor_topics.json,
com guias condicionais de prova, coletivo, cálculo, procedimento e saúde.
Pretensões: labor_claims_index.md e só as entradas escolhidas de labor_claims.json
(90 pretensões, teses do trabalhador e da defesa, autoridades candidatas e marcos
temporais, inclusive a EC 141/2026).
A revisão v4 inclui labor_review com relações, períodos, fontes e questões.
Cálculos são demonstrados com parâmetros explícitos; lacunas ficam por questão.

Atendimento com poucos ou nenhum documento usa labor_intake_rules.md: relato
atribuído pode permitir a inicial com prova futura planejada. Preservar versões,
fazer apenas perguntas materiais e distinguir redação de confirmação probatória.
labor_development_rules.md orienta pretensões, conciliação, prescrição, recursos
e instrução. Selecionar labor_claims/labor_sectors e ler somente os guias pertinentes.

Elaboração tese por tese segue incremental_petition_rules.md: análise-base comum,
mapa de teses, capítulo solicitado, versões preservadas e consolidação no momento
pedido. Novos dados reabrem dependências; não presumir aprovação do usuário.

Execute somente a tarefa solicitada; pergunte apenas quando houver ambiguidade,
conflito ou dado indispensável ausente. Preserve originais e versões, escreva em
narrativa jurídica afirmativa (fatos → provas → questão → norma conferida →
subsunção → contrapontos → pedido), cite fontes por arquivo/página/folha e
nunca invente fatos, prazos ou autoridade jurídica. Não use preenchimentos como
“conforme documentação”, “documento apresentado” ou “certidão analisada”.

Este arquivo é uma ponte para importação por GitHub. As regras completas, os
scripts e os schemas permanecem em `skills/legal-process-parser/`.
