---
name: outcome-tracker
description: "Record the testable predictions inside a decision, then score them against reality later — so frameworks earn trust from outcomes, not vibes. Use when committing to a prioritisation, forecast, or plan (to log what it predicts), when asked to review what actually happened, or to compute how well-calibrated past RICE scores, forecasts, or bets have been."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# outcome-tracker

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

Produces a prediction record at decision time, and a calibration report with per-framework hit rates at review time.
