---
name: data-quality-audit
description: "Audit a dataset for the quality problems that silently break analysis — missingness, duplicates, outliers, type and range errors, consistency, and freshness — and produce a prioritised fix list. Use when asked to assess data quality, audit a dataset, check data before analysis, or explain why numbers look off."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# data-quality-audit

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

Produces a structured quality report across the standard dimensions, the specific issues found (with the checks to run), severity, and how to fix each.
