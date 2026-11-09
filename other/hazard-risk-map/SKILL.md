---
name: hazard-risk-map
description: "Figure out which disasters and emergencies your specific location actually faces — and the concrete prep each one demands — so your readiness targets real risks instead of generic ones. Use when someone says 'what disasters should I prepare for', 'am I in a flood/wildfire/quake zone', 'what emergencies are likely where I live', or 'where do I start with preparedness'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# hazard-risk-map

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

Produces a ranked local-hazard list, the specific prep each demands, warning-signal and alert setup, and where to verify official risk data for your area.
