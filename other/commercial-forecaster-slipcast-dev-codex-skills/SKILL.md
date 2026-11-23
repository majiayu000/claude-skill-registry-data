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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

