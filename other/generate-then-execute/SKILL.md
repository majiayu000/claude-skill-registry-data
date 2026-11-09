---
name: generate-then-execute
description: "Separate raw idea-generation from judgment so creativity isn't strangled by your inner critic — diverge with zero evaluation, then switch to hard critique. Use when asked to brainstorm properly, help me come up with ideas without shutting them down, I keep censoring my own ideas, or separate creating from editing."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# generate-then-execute

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

Produces a pure generation pass (quantity, no judging, no hedging, wild allowed), a clean break, then a separate ruthless critique pass that scores and prunes — because doing both at once produces neither.
