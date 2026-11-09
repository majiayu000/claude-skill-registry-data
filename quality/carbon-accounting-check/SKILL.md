---
name: carbon-accounting-check
description: "Sanity-check a greenhouse gas inventory before it goes into a report or gets audited. Use when asked to review a carbon footprint, check a GHG inventory, validate scope 1/2/3 numbers, explain a year-over-year emissions change, or prepare emissions data for assurance."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# carbon-accounting-check

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

Produces a boundary review, data-quality assessment, emission-factor sensitivity list, YoY bridge, and a fix-before-publishing list.
