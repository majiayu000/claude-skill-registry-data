---
name: api-design-reviewer
description: Comprehensive REST API design review with automated linting, breaking-change
  detection, and design scorecards. Catches inconsistent conventions, missing versioning,
  and design smells before APIs ship. Use when reviewing a PR that adds or changes
  API endpoints, auditing an existing API for v2 migration, or establishing API standards
  for a team.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# api-design-reviewer

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

