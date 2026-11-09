---
name: offer-comparison
description: "Compare two or more job offers as total-comp curves over four years — vesting cliffs, bonuses, 401(k) match, and the crossover year computed, not vibed. Use when asked to compare job offers, which offer pays more over time, model my equity vesting, or is the startup offer actually worth it."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# offer-comparison

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

Produces a year-by-year and cumulative comp table per offer, the crossover analysis, and negotiation levers ranked by dollar impact.
