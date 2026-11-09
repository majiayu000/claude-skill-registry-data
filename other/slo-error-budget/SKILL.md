---
name: slo-error-budget
description: "Define Service Level Objectives (SLOs) and an error budget policy for a service. Use when asked to write SLOs, define SLIs, calculate an error budget, set reliability targets, or create an error budget policy."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# slo-error-budget

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

Produces a complete SLO document with SLI definitions, target calculation, error budget policy, burn rate alerts, and review cadence.
