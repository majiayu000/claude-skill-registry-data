---
name: subcontractor-scorecard
description: "Score a subcontractor's performance across schedule reliability, quality, safety, paperwork, and change-order behaviour with weighted anchors. Use when asked to evaluate a sub, build a subcontractor scorecard, decide whether to rebid or rehire a trade, review sub performance for prequalification, or justify removing a sub from the bid list."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# subcontractor-scorecard

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

Produces a weighted scorecard with per-dimension anchored ratings, evidence notes, and an award/retention recommendation.
