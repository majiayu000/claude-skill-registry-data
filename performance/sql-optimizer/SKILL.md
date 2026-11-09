---
name: sql-optimizer
description: "Diagnose a slow SQL query and produce a concrete optimization plan. Use when asked to optimize SQL, speed up a slow query, reduce a query's cost/scan, fix a timeout, or review a query plan."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# sql-optimizer

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

Produces an analysis — the likely bottleneck, what the plan is doing wrong (full scans, bad joins, spills), the specific rewrite and index/partition changes, and the expected impact, with the optimized query.
