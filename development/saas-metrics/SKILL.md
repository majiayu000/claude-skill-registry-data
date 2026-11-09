---
name: saas-metrics
description: "Compute the core SaaS metrics — MRR/ARR, growth, NRR/GRR, churn, quick ratio, magic number — from your numbers. Use when asked to calculate SaaS metrics, MRR/ARR, net revenue retention, the quick ratio, or to build a SaaS metrics snapshot for a board/investor update."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# saas-metrics

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

Produces a computed metrics dashboard with each value, its benchmark, and a one-line read on what it means.
