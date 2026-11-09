---
name: policy-renewal-review
description: "Run a pre-renewal review of an insurance programme: scan coverage gaps against current operations, test limit adequacy against inflation and exposure growth, read the claims experience into pricing expectations, frame market alternatives, and arm the broker negotiation. Use when asked to prepare for a policy renewal, review cover before renewal, check if limits are still adequate, or build renewal negotiation points."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# policy-renewal-review

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

## Требования к результату

Produces a structured renewal review with gap findings, limit assessment, pricing outlook, and negotiation points.
