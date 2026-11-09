---
name: schedule-monte-carlo
description: "Project completion as a distribution, not a date — Monte Carlo over the task graph. Use when a plan's finish date came from summing 'likely' estimates (it's wrong, mathematically), when leadership needs a commit date, or when you need to know which tasks actually control the timeline."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# schedule-monte-carlo

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

Produces P10/P50/P90 completion, per-task criticality (how often each task sits on the critical path), and a real .xlsx — via the bundled zero-dependency simulator, deterministic with a seed.
