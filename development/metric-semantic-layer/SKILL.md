---
name: metric-semantic-layer
description: "Define a metric in a semantic layer so it means one thing everywhere. Use when asked to define a metric, build a semantic layer / metrics layer entry, stop 'revenue means three things' problems, or write a metric definition for dbt MetricFlow / Cube / LookML."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# metric-semantic-layer

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

Produces a metric definition — exact formula, the base measure & aggregation, dimensions, filters, grain, edge cases, and a tool-ready spec.
