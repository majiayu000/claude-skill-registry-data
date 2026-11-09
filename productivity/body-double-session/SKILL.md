---
name: body-double-session
description: "Set up and run a body-doubling session — using another person's presence (in the room, on a call, or a chat check-in) to start and stay on the task your ADHD brain keeps bouncing off. Use when someone says 'I can't start this task', 'body double with me', 'I only work when someone's around', or has ADHD/executive-dysfunction and a task that won't begin."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# body-double-session

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

Produces a session plan, the exact ask to send a body-double partner, and a solo fallback for when no one's available.
