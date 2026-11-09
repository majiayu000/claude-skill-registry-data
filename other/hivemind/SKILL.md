---
name: hivemind
description: Orchestrate free opencode workers from Claude Code to cut token costs.
  Use when delegating grunt work to a single worker or a parallel swarm (scout/coder/tester)
  with worktree isolation, benchmarking against opencode, or when the user says "spawn
  a worker", "swarm", "delegate to opencode", or "/oc".
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# hivemind

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
