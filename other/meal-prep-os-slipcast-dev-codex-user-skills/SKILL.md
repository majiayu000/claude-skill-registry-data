---
name: meal-prep-os
description: "Turn what's actually in the fridge and 90 minutes on Sunday into a week that mostly feeds itself — a cook-once-eat-thrice batch plan, the component method (bases, proteins, sauces that recombine so leftovers don't bore you), honest food-safety day-counts flagged, and the Thursday problem solved in advance. Use when someone says 'meal prep my week', 'what do I cook with what I have', 'we spend too much on takeaway', or 'I'm sick of eating the same thing four days'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# meal-prep-os

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

Produces the Sunday cook plan, the recombination map, and the shopping delta.
