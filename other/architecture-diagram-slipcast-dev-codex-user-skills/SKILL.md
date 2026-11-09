---
name: architecture-diagram
description: "Diagram a system or technical architecture — services, data stores, and how they connect. Use when asked to draw an architecture, show how components fit together, map a system/data flow, or visualize services and dependencies."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# architecture-diagram

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

Produces a ready-to-render Mermaid diagram with grouped subgraphs (renders live, exportable as PNG/SVG) plus a component legend and notes.
