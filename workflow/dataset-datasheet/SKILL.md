---
name: dataset-datasheet
description: "Document a dataset so others know what it is, how it was made, and when not to use it. Use when asked to write a datasheet for a dataset, document training/eval data, or assess whether a dataset is fit for a use."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# dataset-datasheet

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

Produces a datasheet — motivation, composition, collection process, preprocessing, recommended uses & limits, distribution, and maintenance.
