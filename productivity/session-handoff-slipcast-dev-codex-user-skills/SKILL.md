---
name: session-handoff
description: "Write a handoff summary so another agent or person (or a fresh session) can pick up the work with full context. Use when ending a work session, hitting a context limit, switching agents, or pausing a task mid-flight."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# session-handoff

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

Produces a structured handoff: what the goal is, what's done, the current state, what's next, and the gotchas — so no context is lost across the boundary.
