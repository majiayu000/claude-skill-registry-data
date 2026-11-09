---
name: async-instead
description: "Convert a meeting into async work that actually decides — the doc-plus-deadline format that replaces the room, the comment-window rules, the decision-closure step that async usually fumbles, and the honest test for what still needs synchronous. Use when asked can this meeting be async, replace our status meeting with a doc, run this decision without a call, or async isn't working for us."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# async-instead

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

Produces the conversion design, the async artifact format, the closure protocol, and the still-needs-a-room list.
