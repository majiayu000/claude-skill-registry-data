---
name: model-migration-plan
description: "Plan the migration of an LLM feature from one model to another without breaking production. Use when a model is being deprecated, a newer model looks better or cheaper, or when asked how to upgrade models safely, run shadow traffic, or set rollback criteria for a model change. For choosing which model in the first place use model-selection-advisor."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# model-migration-plan

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

Produces a phased migration plan with eval gates, shadow/canary stages, prompt-adaptation notes, and rollback triggers.
