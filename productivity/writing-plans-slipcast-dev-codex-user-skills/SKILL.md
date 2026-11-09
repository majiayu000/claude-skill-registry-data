---
name: writing-plans
description: "Write an executable work plan BEFORE starting a complex task — decomposed steps with verification points, risks pre-named, and explicit stop conditions — so execution becomes checking boxes instead of improvising. Use when a task will take many steps, when asked to plan before doing, when previous attempts sprawled or stalled, or before delegating work to subagents. Pairs with executing-plans."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# writing-plans

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

Produces a plan document another agent (or future you) could execute without re-deriving the thinking.
