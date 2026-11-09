---
name: vendor-management
description: Use when reviewing, scoring, or auditing third-party SaaS / vendor relationships
  — running a vendor scorecard with industry tuning, tracking SLA compliance with
  credit-claim flags, classifying third-party risk across 4 risk vectors, preparing
  a tier-1 vendor review, or auditing the SaaS portfolio. Forks context so large vendor
  catalogs (50-500 line items) and SLA logs don't pollute the parent thread. Triggers
  on "vendor SLA", "vendor scorecard", "third-party risk", "TPRM", "vendor review",
  "supplier performance", "vendor health check", "renewal review".
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# vendor-management

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

