---
name: shift-schedule-builder
description: "Build a staff shift schedule that matches coverage to demand while hitting a labor-cost target. Use when asked to build a shift schedule, staff a rota, plan coverage for a restaurant/retail/shift-based team, or balance labor cost against service."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# shift-schedule-builder

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

Produces a day-part coverage plan mapped to forecast demand, role-by-role assignments, the projected labor cost vs. target, and the fairness/compliance guardrails (rest between shifts, overtime, availability).
