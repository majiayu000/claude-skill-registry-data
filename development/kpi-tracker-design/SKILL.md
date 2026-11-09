---
name: kpi-tracker-design
description: "Design a KPI tracker that drives decisions instead of decorating them — the few-metrics discipline (5–9, each with an owner and a so-what), targets with honest baselines, the trend-first layout, and the review ritual where the tracker actually gets used. Use when asked set up KPI tracking for the team, build a metrics dashboard in sheets, which numbers should we track, or our dashboard exists but nobody acts on it."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# kpi-tracker-design

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

Produces the metric selection with kill-list, the tracker structure, the target-setting notes, and the review ritual.
