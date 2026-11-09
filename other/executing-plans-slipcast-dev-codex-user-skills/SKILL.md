---
name: executing-plans
description: "Execute a written plan with discipline — verify each step before advancing, surface deviations instead of improvising around them, and keep a visible execution log. Use when working through a plan (yours or another agent's), resuming multi-session work, or when execution keeps drifting from what was agreed. Pairs with writing-plans."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# executing-plans

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

Produces completed work plus an execution log showing what matched the plan, what deviated and why, and what the plan got wrong.
