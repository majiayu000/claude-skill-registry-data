---
name: feature-sunset-plan
description: "Plan the retirement of a product feature — the kill decision made honest, user migration, data handling, comms sequencing, and the code actually deleted. Use when deprecating or sunsetting a feature, killing an underused capability, retiring an AI feature that didn't land, or when a 'deprecated' feature has haunted the codebase for two years. For API deprecation specifically use api-versioning-strategy."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# feature-sunset-plan

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

## Требования к результату

Produces a sunset plan: the decision record, affected-user analysis, migration paths, a staged timeline with comms per stage, and the removal checklist.
