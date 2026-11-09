---
name: event-run-of-show
description: "Build the minute-by-minute run of show that lets an event run without the planner being asked anything — every cue, who owns it, what happens if it slips, and the version each supplier actually needs. Use when asked to write a run of show, event schedule, show flow, or production schedule, or to prepare the day-of timeline for a conference, wedding, launch, or gala."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# event-run-of-show

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

Produces the master timeline with owners and cues, the load-in and load-out schedule, the supplier-specific extracts, the contingency triggers, and the on-the-day contact sheet.
