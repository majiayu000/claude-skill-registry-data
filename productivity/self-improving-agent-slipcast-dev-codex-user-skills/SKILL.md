---
name: self-improving-agent
description: Curate the agent's own memory into durable project knowledge. Reviews
  Claude Code auto-memory (MEMORY.md and its topic files) for learnings worth keeping,
  promotes proven ones into AGENTS.md or .claude/rules/, records a correction as a
  lesson that persists across sessions, prunes stale or duplicate entries, and turns
  a recurring fix into a reusable skill. Use whenever the user asks what you have
  learned or saved about the project, which memories should become permanent rules,
  to remember a lesson or stop repeating a mistake, or to clean up, audit or check
  the health of memory.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# self-improving-agent

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
