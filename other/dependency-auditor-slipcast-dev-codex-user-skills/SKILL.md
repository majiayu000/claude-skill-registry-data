---
name: dependency-auditor
description: 'Audit and manage dependencies across multi-language projects. Identifies
  vulnerabilities, license conflicts, transitive dependency risks, and safe-upgrade
  paths. Use when auditing third-party packages before release, investigating a CVE,
  planning a major version bump, or running a license-compliance review. Examples:
  ''audit our npm dependencies'', ''do we have GPL contamination'', ''plan the upgrade
  to React 19''.'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# dependency-auditor

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

