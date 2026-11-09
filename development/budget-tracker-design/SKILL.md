---
name: budget-tracker-design
description: "Design a budget-vs-actuals tracker that stays alive past February — the category grain that matches real statements, the variance view that answers 'are we okay', the update ritual small enough to survive, and the honest handling of irregular expenses. Use when asked build me a budget spreadsheet, track team spend against budget, why do we always blow the budget invisibly, or design a household/project budget tracker."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# budget-tracker-design

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

Produces the tracker structure, the variance logic, the irregulars ledger, and the monthly fifteen-minute ritual.
