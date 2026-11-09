---
name: escalation-tree
description: "Design a support/incident escalation tree — who handles what, when it escalates, and to whom. Use when asked to design an escalation path, an escalation matrix, support tiers, an on-call escalation policy, or to fix 'tickets bounce around / nothing gets escalated in time'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# escalation-tree

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

Produces an escalation tree — tiers & ownership, severity definitions, time-based triggers, routing rules, contacts/roles, and the customer-communication cadence per level.
