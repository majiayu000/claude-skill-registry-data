---
name: commercial-forecaster
description: Use when building a quarterly bookings forecast, ARR projection, pipeline
  forecast, NRR projection, or commit/best-case/pipe-only board number — especially
  when the CRO needs to walk the board through funnel math + cohort ARR + per-stage
  conversion assumptions without the theatre of a single undefended number. Decomposes
  pipeline into commit, best-case, and pipe-only tiers; projects cohort-level NRR/GRR
  to surface leaky cohorts before they show up in the consolidated number; scores
  per-stage funnel confidence so soft-floor stages get treated differently from high-confidence
  ones. Every output explicitly names the conversion rate used, the data window, and
  the weighting choice. For Head of Commercial, RevOps, VP Sales, and CRO at quarterly
  forecast or board prep. NOT financial close (see finance/financial-analysis). NOT
  strategic CRO hiring/territory (see c-level-advisor/cro-advisor). NOT pricing (see
  sibling pricing-strategist).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# commercial-forecaster

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

