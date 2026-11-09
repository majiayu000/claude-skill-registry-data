---
name: first-90-days-out
description: "Build a concrete plan for the first 90 days after release from incarceration — the ID, benefits, housing, check-ins, and money moves that have to happen in order, before they cascade into a crisis. Use when asked I'm getting out of prison what do I do first, reentry plan, just got released and I'm overwhelmed, or first steps after incarceration. Not legal advice; points to reentry services."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# first-90-days-out

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

Produces a sequenced week-by-week plan for the highest-priority setup (ID and documents, parole/probation compliance, benefits, housing, phone, bank, health/meds), the deadlines that carry real consequences, a triage of what's urgent vs. what can wait, and where to get reentry support.
