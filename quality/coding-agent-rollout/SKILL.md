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
