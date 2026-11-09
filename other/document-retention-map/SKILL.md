---
name: document-retention-map
description: "Decide what documents to keep, for how long, and where — the personal/small-biz retention map by category (tax, legal, medical, warranties, employment), jurisdiction-flagged periods, and the destruction discipline for what's past its date. Use when asked how long do I keep tax documents, can I shred this, set up a document retention system, or what papers does my small business need to keep."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# document-retention-map

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

Produces the category map with keep-periods (flagged verify-locally), the keep-forever list, the digitize rules, and the annual purge ritual.
