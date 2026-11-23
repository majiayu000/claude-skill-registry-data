---
name: workflow-builder
description: Design and write deterministic multi-agent workflow scripts (.js files
  in .claude/workflows/) for Claude Code's Workflow tool. Use when a user wants to
  build, create, author, scaffold, or run a custom Claude Code workflow, orchestrate
  sub-agents (fan-out, pipeline, loop, judge-panel), or automate a repeatable multi-step
  task across fresh-context agents.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# workflow-builder

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
