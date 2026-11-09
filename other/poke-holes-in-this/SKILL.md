---
name: poke-holes-in-this
description: "Get only the weaknesses in something you made — no praise, no encouragement padding, just the holes and how to fix them. Use when asked to poke holes in this, tell me what's wrong with this, critique this honestly, or don't be nice about it."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# poke-holes-in-this

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

Produces a focused list of the real problems in your draft, plan, argument, or code — ranked by severity, each with why it's a problem and a concrete fix — deliberately stripping the 'this is great!' padding that AI and polite humans add and you don't need.
