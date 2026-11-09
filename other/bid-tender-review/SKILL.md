---
name: bid-tender-review
description: "Analyse a construction bid or tender package for scope gaps, risk-shifting exclusions, unit-rate red flags, and front-loading in the schedule of values. Use when asked to review a bid, level bids, check a tender for gaps, compare sub quotes, or vet a schedule of values before award."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# bid-tender-review

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

Produces a structured bid review with a gap register, exclusion risk table, pricing red flags, and an award recommendation with pre-award clarifications.
