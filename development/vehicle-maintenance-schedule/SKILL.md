---
name: vehicle-maintenance-schedule
description: "Build a maintenance schedule for your car so it stays reliable and holds value — the service intervals, the DIY-vs-shop split, and the checks that prevent breakdowns and rip-offs. Use when asked for a car maintenance schedule, what maintenance does my car need, how to keep my car running, or am I being upsold at the mechanic."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# vehicle-maintenance-schedule

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

Produces an interval-based schedule keyed to your vehicle and driving, the essential do-not-skip items, DIY vs professional, seasonal checks, and how to spot unnecessary upsells — flagging that your owner's manual is the authority.
