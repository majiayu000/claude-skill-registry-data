---
name: notion-db-hygiene
description: Clean the user's REAL Notion database — read it, find stale/incomplete/duplicate
  entries, and fix them via the connector — not advice on keeping Notion tidy. Use
  when asked to clean up my Notion database, my tracker is a mess, find the stale
  and duplicate entries, or tidy my projects DB in Cowork. Reads the database via
  the Notion connector, audits for staleness / missing required fields / duplicates
  / status drift, and produces a hygiene-report artifact plus the applied fixes (with
  a preview-and-confirm step before any change).
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# notion-db-hygiene

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

