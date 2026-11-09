---
name: feature-flag-guide
description: "Write a feature flag management guide and lifecycle playbook for a service or team — covering flag taxonomy, creation checklist, rollout strategy, monitoring requirements, cleanup policy, and governance. Use when asked to document feature flag practices, create a flag rollout plan, write a feature flag policy, or guide a team on flag lifecycle management."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# feature-flag-guide

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

Produces a flag lifecycle playbook, taxonomy reference, per-flag creation template, rollout decision tree, and cleanup checklist.
