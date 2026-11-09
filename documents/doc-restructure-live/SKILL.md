---
name: doc-restructure-live
description: Restructure the user's REAL Google Doc — open it, tighten and reorganise
  it, and return a clean version — not advice on how to edit it. Use when asked to
  clean up this doc, restructure my draft in Drive, make this readable, or tighten
  the doc for review in Cowork. Reads the document via the Google Drive/Docs connector,
  applies a structure-and-concision pass (BLUF, one idea per section, cut the filler),
  and produces a restructured-document artifact plus a change summary — as a new copy,
  never overwriting the original.
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# doc-restructure-live

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

