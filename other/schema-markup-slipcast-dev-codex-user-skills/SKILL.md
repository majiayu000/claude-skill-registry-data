---
name: schema-markup
description: "Generate structured-data (Schema.org / JSON-LD) markup to win rich results in search. Use when asked about schema markup, structured data, rich snippets, JSON-LD, or making a page eligible for stars/FAQ/breadcrumb results."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# schema-markup

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

Produces valid JSON-LD for the right schema type, the rich-result it targets, required vs. recommended fields, and validation/guideline notes.
