---
name: agent-memory
description: Use when a project's AGENTS.md has grown past what anyone reads and you
  want the agent to learn durable facts from its own sessions instead — or when asking
  why the agent keeps re-learning the same correction, why a remembered rule is wrong,
  or where a memory line came from. Implements a four-tier store (L0 transcripts /
  L1 candidates / L2 project context / L3 stable persona) where promotion is earned
  by recurrence across sessions and days, never by one confident statement, and nothing
  reaches a committed file without a human adopting it.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# agent-memory

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

