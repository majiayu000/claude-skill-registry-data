---
name: grocery-budget-audit
description: "Find where the food money actually goes — a no-shame ledger built from real receipts/statements, the four leak categories (waste, convenience markup, brand autopilot, the takeaway blur), a per-leak fix with realistic savings ranges, and a target budget that survives real life. Use when someone says 'we spend how much on food?!', 'audit my grocery spending', 'cut our food bill', or takeaway guilt is the household argument."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# grocery-budget-audit

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

Produces the ledger, the leak report, and a keep-the-joy budget.
