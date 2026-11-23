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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

