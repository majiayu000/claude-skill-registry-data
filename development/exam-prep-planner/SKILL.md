---
name: exam-prep-planner
description: "Build a realistic exam-prep schedule with spaced repetition and retrieval practice — the plan that survives contact with an actual week. Use when asked to plan my exam prep, make a study schedule, I have N weeks until finals, or how do I study for multiple exams."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# exam-prep-planner

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

Produces a day-by-day plan across all exams: spaced blocks, retrieval-first sessions, weak-topic weighting, and built-in slack for the days that go wrong.
