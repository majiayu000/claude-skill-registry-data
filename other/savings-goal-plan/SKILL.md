---
name: savings-goal-plan
description: "Turn a savings goal into a month-by-month funding plan. Use when asked to save for something (emergency fund, house deposit, trip, big purchase), or to figure out how much to set aside each month. Educational, not regulated financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# savings-goal-plan

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

Produces the required monthly contribution, a timeline, milestones, and trade-offs if the target date is too aggressive.
