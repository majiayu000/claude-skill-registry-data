---
name: customer-incident-update
description: "Write the customer-facing incident update during an outage — status-page post or email — that's honest about impact without over-promising. Use when asked to write a status page update, draft customer comms for an outage, post an incident notice, or tell customers about downtime. Distinct from incident-postmortem (the internal retro)."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# customer-incident-update

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

Produces the update in the right tense for the incident stage (investigating / identified / monitoring / resolved), with impact scope, any workaround, and a concrete next-update time.
