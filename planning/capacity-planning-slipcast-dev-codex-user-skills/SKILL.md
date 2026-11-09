---
name: capacity-planning
description: "Produce a capacity planning document for a service covering traffic forecasts, resource requirements, and scaling strategy. Use when asked to plan infrastructure capacity, forecast resource needs, model traffic growth, define scaling strategy, or produce a capacity review for a service."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# capacity-planning

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

Produces a structured capacity plan covering current baseline metrics, growth projections, resource requirements per tier, scaling strategy, cost projections, capacity triggers, and an infrastructure action roadmap.
