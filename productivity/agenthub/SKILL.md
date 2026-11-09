---
name: agenthub
description: 'Multi-agent collaboration plugin that spawns N parallel subagents competing
  on the same task via git worktree isolation. Agents work independently, results
  are evaluated by metric or LLM judge, and the best branch is merged. Use when: user
  wants multiple approaches tried in parallel — code optimization, content variation,
  research exploration, or any task that benefits from parallel competition. Requires:
  a git repo.'
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# agenthub

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
