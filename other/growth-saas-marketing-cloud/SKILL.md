---
name: growth-saas-marketing-cloud
description: Projetar e evoluir SaaS de growth, marketing cloud, analytics e PLG com
  foco em UX orientada a decisao, metricas de negocio, modelagem de eventos, dashboards,
  graficos, tabelas, motores de insight acionavel e orquestracao de campanhas. Use
  quando Codex precisar definir arquitetura de produto, fluxos, informacao exibida,
  componentes analiticos, semantica de metricas, recomendacoes, inteligencia explicavel,
  GaaS Afinz, CRM, midia paga, templates, activity_names, ordem de disparo, AppsFlyer,
  Supabase ou governanca de dados de marketing.
metadata:
  version: 1.0.0
  origin: codex
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Produto
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Growth SaaS Marketing Cloud

## Objetivo

Projetar software analitico como product engineer senior, partindo da decisao de negocio e descendo para metricas, eventos, UX, componentes visuais, servicos de inteligencia e governanca operacional.

Para GaaS Afinz, tratar o produto como sistema de decisao operacional, nao como BI decorativo: o operador deve entender estado, causa provavel, evidencia, acao e confianca em poucos minutos.

## Fluxo Base

1. Identificar a decisao que o produto precisa destravar.
2. Mapear o modelo de negocio e a arvore de metricas.
3. Definir a semantica de dados: entidades, eventos, propriedades, janelas de tempo e filtros.
4. Desenhar a UX em camadas: glance, scan, drill, acao e auditoria.
5. Escolher graficos, tabelas e controles sem desperdiçar densidade cognitiva.
6. Definir o motor de inteligencia: deteccao, diagnostico, recomendacao, explicabilidade e priorizacao.
7. Entregar a resposta em linguagem de produto, com recomendacoes implementaveis e limites claros.

## Regra Principal

Nunca comecar por "qual grafico usar". Comecar por:

- Qual decisao o operador precisa tomar em ate 2 minutos.
- Qual metrica muda a prioridade do negocio.
- Quais alavancas o time consegue mover.
- Qual acao o sistema deve sugerir depois da leitura.
- Qual e a confianca da leitura e qual dado limita a conclusao.

Se a resposta nao altera uma decisao, o modulo e decorativo.

Para operacoes CRM/midia, preferir a cadeia:

`Sinal -> Impacto -> Causa provavel -> Evidencia -> Acao -> Confianca`

## Perguntas Obrigatorias

Antes de propor arquitetura ou UX, responder explicitamente:

- Quem usa: operador, analista, lider, executivo, CS, midia, CRM, revenue.
- Com que frequencia: tempo real, diario, semanal, mensal.
- Qual e a unidade de analise: conta, campanha, jornada, segmento, canal, template, activity_name, experimento, coorte.
- Qual e a metrica norte e quais sao as metricas driver.
- O que e diagnostico, o que e acao e o que e apenas auditoria.
- O que precisa ser comparado: meta, periodo anterior, baseline, cohort, benchmark, safra ou familia historica.
- Qual dado e confirmado, direcional, suspeito ou bloqueado.

## Como Estruturar a Solucao

Organizar a interface em quatro camadas:

- Contexto: estado atual, delta, meta, tendencia, anomalia e freshness.
- Diagnostico: por que mudou, em que dimensao, em que etapa, com qual evidencia e confianca.
- Acao: o que fazer agora, impacto esperado, risco, prazo, dono e criterio de sucesso.
- Auditoria: fonte, regra aplicada, amostra, conflitos, historico e reversao.

Preferir sempre uma narrativa do tipo:

`Padrao -> Impacto -> Causa provavel -> Oportunidade -> Atalho`

Exemplo:

`Share de CRM caiu 8pp na semana. A perda veio de WhatsApp em reativacao. Abertura manteve, clique caiu. Recomendar teste de oferta e ajuste de copy nas proximas 72h. Confianca media: base completa, mas baixo volume.`

## Leitura Progressiva das Referencias

Ler apenas o necessario:

- Ler [references/foundations.md](references/foundations.md) quando a tarefa envolver modelo de negocio, North Star, metric tree, funnel, loop de crescimento, eventos ou taxonomia.
- Ler [references/ux-analytics.md](references/ux-analytics.md) quando a tarefa envolver layout, estados, interacao, command palette, drawer, filtros, empty/loading/error, densidade, performance de conteudo ou UX operator-owner.
- Ler [references/visualization.md](references/visualization.md) quando a tarefa envolver escolha de graficos, tabelas, formatacao numerica, cores, acessibilidade ou performance visual.
- Ler [references/architecture.md](references/architecture.md) quando a tarefa envolver arquitetura de inteligencia, semantic layer, insights, recomendacoes, explainability ou pipeline analitico.
- Ler [references/afinz-gaas-operating-model.md](references/afinz-gaas-operating-model.md) quando a tarefa envolver GaaS Afinz, CRM, midia paga, Supabase, operador, relatorios, orquestrador ou decisoes de produto especificas da operacao.
- Ler [references/afinz-crm-communications.md](references/afinz-crm-communications.md) quando a tarefa envolver aba Comunicacoes, templates, assets, previews, activity_names, Salesforce Marketing Cloud, AppsFlyer ou governanca de links.
- Ler [references/dispatch-order-intelligence.md](references/dispatch-order-intelligence.md) quando a tarefa envolver sugestoes inteligentes, ordem de disparo, reguas, sequencia D01/D02, S1D01, dispXsY, matching semantico ou reuso de templates.
- Ler [references/measurement-and-data-quality-guardrails.md](references/measurement-and-data-quality-guardrails.md) quando a tarefa envolver CAC, CPA, atribuicao, dados parciais, freshness, confianca, rentabilizacao, Opt-in Copa Visa ou recomendacoes baseadas em metricas.
- Ler [references/gaas-funnel-analytics-pattern.md](references/gaas-funnel-analytics-pattern.md) ao criar ou evoluir Funil de Aquisição, Funil B2C, Funil de Mídia Paga ou uma síntese Growth entre funis.

## Padroes de Entrega

Quando a solicitacao for conceitual, responder nesta ordem:

1. Problema de negocio.
2. Modelo de dados e metricas.
3. UX e informacao.
4. Componentes e interacoes.
5. Inteligencia e recomendacoes.
6. Riscos, tradeoffs e proximo corte de implementacao.

Quando a solicitacao for de implementacao, produzir:

- contrato de dados ou tipos
- diagrama de fluxo ou estrutura de modulos
- componentes e responsabilidades
- regras de insight e priorizacao
- estados sistemicos e criterios de sucesso
- plano de validacao proporcional ao risco

## Heuristicas Fixas

- Mostrar numero grande sem delta e proibido.
- Mostrar delta sem baseline e insuficiente.
- Mostrar insight sem acao e incompleto.
- Mostrar alerta sem severidade e sem recuperacao e ruido.
- Mostrar mais de quatro series simultaneas em um mesmo grafico geralmente e erro.
- Usar tabela quando o usuario precisa comparar, ordenar, filtrar, exportar ou agir linha a linha.
- Usar grafico quando o usuario precisa perceber forma, tendencia, distribuicao, relacao ou contribuicao.
- Usar drawer e nao navegacao completa quando o contexto atual precisa ser preservado.
- Colocar filtros como barra persistente e chips visiveis; nao esconder estado do sistema.
- Tratar metricas de negocio como objetos semanticos, nao como colunas soltas.
- Para GaaS, sugestao inteligente sem explicacao, confianca e acao manual revisavel e incompleta.
- Para CRM, nunca confundir `template_id` com `activity_name`: template e conteudo; activity_name e execucao.
- Para midia, nunca tratar CPA de plataforma como CAC de cartao.
- Para dados operacionais, diferenciar confirmado, direcional, suspeito e bloqueado.

## Anti-Padroes

- Dashboard corporativo generico que so empilha cards e graficos.
- KPI sem dono, sem janela temporal ou sem formula.
- Cor decorativa confundida com semantica.
- Painel que descreve o problema mas nao aponta proxima acao.
- Dependencia de tooltip para compreender a tela.
- Drill-down que faz o usuario perder contexto ou resetar filtros.
- Insight gerado sem indicar confianca ou origem.
- "IA" que sugere sem mostrar regra, score, amostra e motivo.
- Automacao que escreve no banco sem governanca, revisao ou rollback.

## Benchmarks Mentais

Pensar por referencia de categoria:

- Amplitude e Mixpanel para analise comportamental, funnels, segmentacao e metric trees.
- Stripe para produtividade operacional, busca, atalhos e tabelas densas.
- Linear para foco, velocidade, clareza e keyboard-first.
- Atlassian e MUI para acessibilidade, grids, tabelas e tokens de sistema.
- ECharts ou biblioteca equivalente quando a complexidade visual exigir mais do que o charting basico.
- Para GaaS Afinz, usar o vault Obsidian como ontologia operacional e o Supabase como fonte viva; snapshots do vault sao contexto, nao verdade eterna.

Usar benchmark como principio, nao como copia visual cega.

## Saida Esperada

Toda proposta deve deixar claro:

- que decisao o sistema destrava
- que metrica move o negocio
- que evento ou entidade alimenta a analise
- que visualizacao prova o argumento
- que recomendacao o usuario consegue executar depois
- qual e a confianca, a fonte e o limite da recomendacao
