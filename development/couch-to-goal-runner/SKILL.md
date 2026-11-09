---
name: couch-to-goal-runner
description: "Build a beginner running plan from wherever you are to a real goal — first nonstop mile, 5K, or 10K — that builds up slowly enough to avoid injury. Use when asked for a couch to 5k plan, help me start running, train for a [distance], or a running plan for beginners."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# couch-to-goal-runner

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

Produces a week-by-week walk/run progression to the goal, session detail, pacing and form basics, rest and cross-training, and an injury-prevention note — with a 'check with a doctor if you have health conditions' flag.
