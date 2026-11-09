---
name: data-quality-checks
description: "Design the data quality checks for a table or pipeline across the standard dimensions. Use when asked to add data quality tests, define DQ checks, catch bad data before it hits dashboards, or set up monitoring for a dataset."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# data-quality-checks

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

Produces a checks plan across completeness, validity, uniqueness, freshness, consistency, and accuracy — each with the rule, severity, and where it runs (dbt test / Great Expectations / SQL assertion).
