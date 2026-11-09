---
name: exam-study-plan
description: "Build a backward-planned study schedule for an exam — using proven learning methods, not just re-reading — so you cover what matters and actually retain it. Use when asked to make a study plan, help me study for [exam], I have an exam in [time], or how do I revise."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# exam-study-plan

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

Produces a week-by-week plan working back from the exam date, prioritized by weighting and your weak spots, sessions built on active recall and spaced repetition, past-paper/practice integration, and a realistic pace with breaks — not an unsustainable cram that forgets everything by exam day.
