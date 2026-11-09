---
name: churn-analysis
description: "Produce a structured churn analysis that separates avoidable from unavoidable churn. Use when investigating why customers are leaving, identifying at-risk segments, calculating net revenue retention, or building a retention intervention plan."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# churn-analysis

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

Produces a churn report with rate calculations, categorised reasons by avoidability, segment breakdown, timing analysis, early warning signals, and prioritised interventions ranked by estimated impact.
