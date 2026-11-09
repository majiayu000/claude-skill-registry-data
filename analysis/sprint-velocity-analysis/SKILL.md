---
name: sprint-velocity-analysis
description: "Analyze sprint velocity data and produce an engineering team health report covering delivery trends, capacity utilization, and improvement recommendations. Use when asked to analyze sprint velocity, review team delivery health, identify delivery risks, or produce a retrospective data analysis."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# sprint-velocity-analysis

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

Produces a velocity trend analysis, health diagnosis table, top improvement recommendations with implementation steps, and a next-sprint capacity forecast.
