---
name: subscription-auditor
description: "Find the subscriptions you forgot you pay for — a tool-using agent audits statements and inboxes, prices the waste annually, and preps (never executes) the cancellations. Use when asked to audit my subscriptions, find recurring charges, what am I paying for, or help me cancel unused services."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# subscription-auditor

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

Produces the subscription inventory with keep/cancel/downgrade verdicts, the annual-waste number, and approval-gated cancellation prep.
