---
name: chart-data-extractor
description: "Extract pixel-level data from an image of a chart or graph and produce a structured data table. Use when asked to extract data from a chart image, transcribe numbers from a graph, digitise a chart, or turn a screenshot of data into a table. Best used with Claude Opus 4.7 or newer for reliable chart data extraction."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# chart-data-extractor

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

Produces a structured table with extracted values, confidence levels, and a reconstructed chart source.
