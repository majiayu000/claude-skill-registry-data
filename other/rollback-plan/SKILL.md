---
name: rollback-plan
description: "Write a concrete rollback plan for a risky change (deploy, migration, feature-flag flip, config rollout) so the reverse is one command away — not an improvised debate at 2am. Use when asked to write a rollback plan, back-out plan, revert plan, or 'what if we need to undo this'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# rollback-plan

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

Produces a rollback plan with the signals that trigger it, exact reverse commands, verification steps, data-safety notes, and a communications template.
