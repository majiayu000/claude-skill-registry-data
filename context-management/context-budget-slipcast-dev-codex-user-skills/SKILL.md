---
name: context-budget
description: "Plan a session's context window like the budget it is — what loads up front, what gets linked instead, what stays fetch-on-demand, and how to keep the stable prefix cache-friendly so repeated turns cost cents instead of dollars. Use when asked my agent keeps blowing its context, plan what to load into the session, why is every turn so expensive, or design the context for this workflow."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# context-budget

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

Produces the load/link/fetch allocation, the cache-aware prefix layout, the per-turn cost shape, and the eviction rules for when the window fills anyway.
