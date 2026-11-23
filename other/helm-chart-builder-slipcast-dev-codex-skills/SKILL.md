---
name: helm-chart-builder
description: 'Helm chart development agent skill and plugin for Claude Code, Codex,
  Gemini CLI, Cursor, OpenClaw — chart scaffolding, values design, template patterns,
  dependency management, security hardening, and chart testing. Use when: user wants
  to create or improve Helm charts, design values.yaml files, implement template helpers,
  audit chart security (RBAC, network policies, pod security), manage subcharts, or
  run helm lint/test.'
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# helm-chart-builder

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
