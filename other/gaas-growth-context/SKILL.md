---
name: gaas-growth-context
description: Preparar o Growth Context Pack para reports Afinz/GaaS, Report Live,
  CRM aquisicao, midia paga, seguros, Plurix/B2B2C, contratos de views/slides, perfis
  de output semanal/mensal/deep dive, storytelling growth, skip_llm e governanca de
  metricas. Use quando Codex precisar sintetizar repo, vault Obsidian, Supabase, planilha-mestre,
  assets de apresentacao ou briefing em uma camada semantica operacional antes de
  gerar textos, slides, tabelas, action queues ou payloads de publicacao do Report
  Live.
metadata:
  version: 1.0.0
  origin: codex
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Contexto para IA
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# GaaS Growth Context

## Objetivo

Gerar um Growth Context Pack antes de qualquer report Afinz/GaaS. A skill nao substitui SQL, planilha, Supabase ou Report Live: ela organiza contexto, contrato de views, perfis de output, guardrails, narrativa e textos permitidos para que o report nao vire uma colecao solta de tabelas.

Regra central: numeros vem de Supabase/SQL/views; a LLM escreve apenas prosa, diagnostico, recomendacao e limites de leitura.

## Workflow

1. Definir ou inferir o `report_profile` antes de selecionar slides.
2. Ler os invariantes de Report Live em `references/report-live-invariants.md`.
3. Ler `references/output-profiles.md` para configurar janela, comparacao, profundidade e blocos.
4. Ler `references/growth-slide-view-contract.md` quando precisar mapear slides, tabelas, colunas ou ordem tecnica.
5. Ler `references/storytelling-growth.md` quando precisar escrever narrativa ou ordenar a apresentacao.
6. Ler `references/metric-dictionary.md` antes de interpretar KPI, delta, CAC, CPA, CPL, funil ou pacing.
7. Ler `references/supabase-source-map.md` antes de consultar ou especificar fontes vivas.
8. Ler `references/data-quality-guardrails.md` antes de concluir, recomendar escala, bloquear leitura ou classificar confianca.
9. Ler `references/asset-patterns.md` quando a tarefa envolver PPTX/PDF/XLSX, deck, planilha-mestre ou layout de slides.
10. Ler `references/ai-analytics-benchmarks.md` quando precisar contrapor a arquitetura com referencias externas de semantic layer, agentic analytics ou data storytelling.
11. Ler `references/output-contract.md` para produzir o Growth Context Pack, `TEXT_REGISTRY_FOR_SKIP_LLM` ou action queues.

## Report Profile

Nunca assumir que o output e mensal. Todo trabalho deve declarar um perfil:

```yaml
report_profile:
  output_type: weekly_impact_cutoff
  audience: lideranca_operacional
  analysis_window: current_week_monday_to_latest_closed_day
  comparison_window: previous_week_same_weekdays
  context_window: month_to_date_until_latest_closed_day
  data_cutoff_rule: latest_closed_day_available
  narrative_mode: acompanhamento_growth
  depth: standard
```

Se o usuario pedir "sexta com dados ate quarta", usar:

- janela analisada: segunda ate o ultimo dia fechado disponivel;
- comparacao principal: mesmos dias da semana anterior;
- contexto auxiliar: mes acumulado ate o mesmo corte;
- proibicao: nao comparar semana parcial com semana cheia como conclusao principal.

## Saida Padrao

Produzir, conforme a tarefa pedir:

- `GROWTH_CONTEXT_PACK.md`
- `VIEW_CONTRACT_NORMALIZED.tsv` ou JSON equivalente
- `NARRATIVE_PLAN.md`
- `TEXT_REGISTRY_FOR_SKIP_LLM.json`
- `ACTION_QUEUE_SCHEMA.tsv`
- `DATA_QUALITY_NOTES.md`

Se for uma resposta em chat, manter a mesma estrutura em texto, sem inventar numeros.

## Scripts

Use `scripts/normalize_view_contract.py` para transformar uma TSV de views/slides em JSON ou TSV normalizada.

Use `scripts/scan_growth_context.py` para inventariar arquivos relevantes no repo/vault antes de montar um pack novo.

Quando a tarefa exigir dado vivo, usar a skill/ferramenta de Supabase disponivel no ambiente. Os scripts desta skill nao devem embutir credenciais nem substituir consultas governadas.

## Guardrails Fixos

- Nao escrever numero que nao venha de dados.
- Nao tratar delta como obrigacao de dizer melhorou ou piorou; delta e campo auxiliar.
- Nao tratar CPA de plataforma como CAC.
- Nao inferir cartao, receita ou CAC de rentabilizacao por clique.
- Nao comparar janelas parciais com janelas cheias como conclusao principal.
- Nao misturar Plurix/B2B2C como bloco externo quando o pedido for Aquisicao CRM; tratar como parte da inteligencia de aquisicao.
- Resumir seguros como inteligencia conectada a CRM e midia, salvo pedido explicito de deep dive.
- Diferenciar evidencias confirmadas, direcionais, suspeitas e bloqueadas.
- Para Report Live, respeitar `skip_llm`: textos entram prontos; dados e graficos vem das views.
- Para publicacao Report Live, preparar payload compativel com `report-sync`, `skip_llm:true`, pg_net e validacao posterior em `report_runs`.
