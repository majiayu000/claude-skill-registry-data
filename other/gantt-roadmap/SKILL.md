---
name: gantt-roadmap
description: "Turn a plan or set of milestones into a timeline / Gantt chart. Use when asked to build a roadmap, schedule phases, show a project timeline, or visualize what happens when."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# gantt-roadmap

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

Produces a ready-to-render Mermaid Gantt chart (renders live, exportable as PNG/SVG) — and, because it has real dates, the result also exports to a calendar (.ics) — plus notes on the critical path and risks.
