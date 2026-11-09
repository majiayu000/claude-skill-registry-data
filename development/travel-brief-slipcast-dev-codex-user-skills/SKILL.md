---
name: travel-brief
description: "Turn a business trip into a one-page brief that runs itself — the itinerary with buffers and failure modes, the meeting logistics pre-solved (addresses, contacts, backup numbers), the packing-and-prep list by trip type, and the expense capture set up before departure. Use when asked prep my business trip, build the travel brief, I always forget something when traveling, or organize this three-city week."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# travel-brief

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

Produces the one-page brief: timeline with buffers, the per-meeting logistics, the contingency card, and the expense setup.
