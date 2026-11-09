---
name: brief-builder
description: "Interview the user with sharp, one-at-a-time questions to turn a vague request into a tight, complete brief any other skill can run on. Use when a request is fuzzy, under-specified, or 'help me think this through', or before running a skill that needs inputs the user hasn't given."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# brief-builder

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

Produces a structured brief (goal, audience, constraints, success criteria) and hands off to the right skill — by interrogating, not guessing.
