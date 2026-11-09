---
name: cohort-curve-model
description: "Fit a retention curve to observed cohort data and project LTV — computed, not estimated. Use when someone has real cohort retention numbers (month 0, 1, 2…) and asks what lifetime value, lifetime periods, or long-run retention they imply, or whether retention is flattening or leaking."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cohort-curve-model

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

Produces a fitted power curve (parameters, R², retention floor), a 24-36 period projection, and a real .xlsx with live formulas where editing ARPU recalculates LTV — via the bundled zero-dependency script.
