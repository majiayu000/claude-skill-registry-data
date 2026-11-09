---
name: flowchart
description: "Turn a process, workflow, or decision logic into a clean flowchart. Use when asked to diagram a process, map a workflow, visualize steps/branches, or show 'how this works' as a chart."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# flowchart

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

Produces a ready-to-render Mermaid flowchart (renders live in the playground, exportable as PNG/SVG) plus a short legend and the assumptions made.
