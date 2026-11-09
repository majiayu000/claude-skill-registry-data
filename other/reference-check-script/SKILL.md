---
name: reference-check-script
description: "Run a rigorous candidate reference check that surfaces real signal. Use when asked to prepare or conduct reference calls for a job candidate, design reference questions, or build a reference-check rubric."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# reference-check-script

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

Produces a structured question set, probing follow-ups, a red/yellow/green scoring rubric, and the legal guardrails — designed to get past 'they were great' without leading the referee.
