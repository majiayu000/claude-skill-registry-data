---
name: ai-roi-audit
description: "Audit whether the organisation's AI spend actually paid — measured against baselines, not vendor math or vibes. Use when a CFO asks what the AI tools returned, when renewing AI contracts, when consolidating overlapping AI subscriptions, or to build the measurement plan before the next spend. To forecast ROI before an investment use roi-estimator; this skill measures what already happened."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-roi-audit

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

Produces an ROI audit with per-tool verdicts (keep/consolidate/cut), the honest-measurement method behind each number, and a baseline plan for whatever can't be scored yet.
