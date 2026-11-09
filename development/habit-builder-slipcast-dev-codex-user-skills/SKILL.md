---
name: habit-builder
description: "Design one habit so it actually sticks — small enough to be unmissable, anchored to something you already do, with a plan for the days you slip. Use when asked to build a habit, help me stick to [habit], I keep failing at [routine], or start a new habit."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# habit-builder

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

Produces a shrunk-down version of the habit, a concrete cue/anchor and time/place, a tracking method, a friction plan (make good easy, bad hard), and a get-back-on-track rule so one miss doesn't end it.
