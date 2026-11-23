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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
