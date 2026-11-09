---
name: handoff
description: Compact the current conversation into a handoff document for another
  agent to pick up, referencing existing artifacts (PRDs, plans, ADRs, issues, commits,
  diffs) by path or URL instead of duplicating them. Use whenever the user wants to
  hand off to a fresh agent, is ending a session mid-task, asks for a handoff doc
  or a summary of state, decisions and next steps for the next session, or starts
  a new session that picks up prior work.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# handoff

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

