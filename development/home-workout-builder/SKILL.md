---
name: home-workout-builder
description: "Build a home workout plan that fits your gear, time, and goal — a real weekly structure, not a random list of exercises. Use when asked to build a home workout, make me a workout plan, exercise routine at home, or how do I work out with no gym."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# home-workout-builder

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

Produces a weekly plan matched to your equipment and schedule, each session with warm-up, main work, sets/reps, and progression, swaps for missing gear, and a way to make it harder over time — with a plain 'this isn't medical advice, stop if it hurts' note.
