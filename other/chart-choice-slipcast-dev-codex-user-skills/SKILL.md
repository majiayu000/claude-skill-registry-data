---
name: chart-choice
description: "Pick the chart the data and the point actually need — the question-to-chart mapping (comparison, trend, composition, distribution, relationship), the honesty rules (axes, baselines, dual-axis traps), and the one-chart-one-point discipline. Use when asked what chart should I use, make this data visual, why does this chart feel misleading, or fix this graph for the deck."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# chart-choice

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

Produces the chart verdict with its reasoning, the honesty checklist applied, and the labeling that lets the chart travel without its author.
