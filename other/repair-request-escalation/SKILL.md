---
name: repair-request-escalation
description: "Get a landlord to actually fix things — the repair request that creates a record, the escalation ladder from reminder to habitability leverage, and the jurisdiction-flagged map of tenant remedies with their prerequisites. Use when asked my landlord won't fix anything, write a repair request, how long can they ignore a broken heater, or what are my options if repairs never happen."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# repair-request-escalation

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

Produces the documented request, the severity triage, the escalation ladder with letters, and the remedies decode with the do-not-DIY warnings.
