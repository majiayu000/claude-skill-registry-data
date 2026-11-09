---
name: is-this-actually-good
description: "Get an honest verdict on whether something you made is actually good — not the reflexive 'this is great!' but a real, criteria-based judgment. Use when asked is this actually any good, be honest is this good enough, rate this honestly, or don't just say it's great."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# is-this-actually-good

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

Produces a grounded assessment against real standards for the format, a clear verdict (great / good / fine / not there yet), the specific things holding it back from the next level, and what it would take to get there — deliberately overriding AI's flattery default.
