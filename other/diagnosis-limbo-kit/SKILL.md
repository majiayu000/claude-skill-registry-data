---
name: diagnosis-limbo-kit
description: "Run the multi-year campaign of being chronically ill with no diagnosis — track patterns across specialists so nothing resets, avoid the 'it's just anxiety' dead-end, chase referrals that stall, and arrive at each new doctor with the longitudinal case instead of starting from zero again. Use when someone says 'I've been sick for years and no one can tell me why', 'every specialist starts over', 'they keep saying it's stress', or is stuck in diagnostic limbo. Not medical advice — it organizes YOUR information so clinicians can use it."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# diagnosis-limbo-kit

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

Produces a longitudinal symptom dossier, a specialist-handoff brief, and a next-move plan.
