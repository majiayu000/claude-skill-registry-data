---
name: bom-cost-review
description: "Review a bill of materials for cost, risk, and supply exposure — cost rollup, top-10 cost drivers, single-source and EOL risk, MOQ vs forecast mismatch, cost-down candidates, and tariff/logistics sensitivity. Use when asked to review a BOM, find cost-down opportunities, check component sourcing risk, or sanity-check BOM cost against target."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# bom-cost-review

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

Produces a structured BOM review with a cost driver Pareto, risk flags per line, and a prioritised cost-down list.
