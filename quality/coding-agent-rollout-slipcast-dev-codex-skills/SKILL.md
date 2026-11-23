---
name: coding-agent-rollout
description: Use when rolling Claude Code out to a team or organization, or auditing
  a rollout already under way — writing or reviewing shared and managed settings.json
  permissions, deciding which MCP servers, plugins and marketplaces to approve, cleaning
  up layered AGENTS.md files, or measuring whether the team actually uses it. Lints
  settings across scopes, inventories every MCP server and plugin against an approved
  list, resolves AGENTS.md layers and imports, and turns local session data into privacy-safe
  adoption counts.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# coding-agent-rollout

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
