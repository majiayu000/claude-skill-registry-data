---
name: exit-waterfall
description: "Compute who gets what at each exit price from a cap table — liquidation preferences, conversion points, and where the founders' share collapses. Use when asked to model an exit waterfall, what do I get if we sell for X, explain liquidation preferences on my cap table, or compare payouts across exit prices."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# exit-waterfall

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

Produces a per-stakeholder payout table across exit values with conversion decisions shown, plus the plain-English reading of what the structure means for each party.
