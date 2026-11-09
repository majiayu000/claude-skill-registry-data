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
