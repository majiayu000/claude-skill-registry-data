---
name: pivot-analysis-planner
description: "Plan pivot-table analysis that answers the actual question — the question-to-layout mapping (rows, values, filters chosen on purpose), the data-shape check that pivots require, and the drill-down path from summary to so-what. Use when asked analyze this data with a pivot, what's driving the total, break this down by category and month, or my pivot shows nonsense."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# pivot-analysis-planner

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

Produces the question decomposition, the pivot layout(s) with reasons, the data-shape fixes needed first, and the reading guide.
