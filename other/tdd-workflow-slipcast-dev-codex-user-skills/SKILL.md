---
name: tdd-workflow
description: "Drive a feature with a disciplined test-driven development loop — red, green, refactor. Use when implementing a feature or fixing a bug and you want tests to lead, or when asked to 'do this with TDD' / write the test first."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# tdd-workflow

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

Produces a step-by-step red-green-refactor plan: the failing test to write first, the minimal code to pass it, and the refactor — one small cycle at a time.
