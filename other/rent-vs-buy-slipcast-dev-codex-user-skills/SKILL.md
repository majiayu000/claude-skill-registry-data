---
name: rent-vs-buy
description: "Model rent-vs-buy honestly — year-by-year net position for both paths including the assumption everyone drops (the renter invests the difference), with a breakeven horizon instead of a verdict. Use when asked should I rent or buy, does buying beat renting in my city, when does buying break even, or run the rent-vs-buy numbers."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# rent-vs-buy

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

Produces the year-by-year comparison table, the breakeven year, the assumption list with defaults labeled, and the not-modeled list.
