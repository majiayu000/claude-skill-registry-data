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
