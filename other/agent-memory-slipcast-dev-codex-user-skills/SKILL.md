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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

