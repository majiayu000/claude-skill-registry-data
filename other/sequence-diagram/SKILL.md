---
name: sequence-diagram
description: "Diagram an interaction as a sequence of messages between participants over time. Use when asked to show an API flow, request/response, auth handshake, integration, or 'what calls what in what order'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# sequence-diagram

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

Produces a ready-to-render Mermaid sequence diagram (renders live, exportable as PNG/SVG) plus notes on edge cases and failure paths.
