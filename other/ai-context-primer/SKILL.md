---
name: ai-context-primer
description: "Build the context an AI needs to do a task well — the background, constraints, examples, and format it can't guess — so you get a great result on the first try instead of a generic one you have to keep correcting. Use when asked why does AI give me generic answers, how do I give AI better context, my AI results are mediocre, or how do I get it right the first time."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-context-primer

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

Produces the specific context this task needs (who/what/constraints/examples/format), a reusable primer you can paste ahead of the request, the difference between a starved prompt and a well-briefed one, and what to leave out — turning vague back-and-forth into a strong first result.
