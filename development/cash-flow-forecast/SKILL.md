---
name: cash-flow-forecast
description: "Build a short-term (13-week) cash flow forecast to see if you can cover what's due. Use when asked to build a cash flow forecast, a 13-week cash flow, a cash projection, or to plan around a cash crunch. Not financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cash-flow-forecast

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

Produces a week-by-week forecast structure — opening cash, expected inflows, scheduled outflows, net movement, and closing/low-point — with the formulas and a worked example, plus the levers if cash goes tight.
