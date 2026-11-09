---
name: comparative-market-analysis
description: "Build a comparative market analysis (CMA) to price a property. Use when asked to do a CMA, a comparative market analysis, price a home, or estimate a property's value from comparables. Not a formal appraisal."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# comparative-market-analysis

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

Produces a structured CMA — the subject property, selected comparables with adjustments, an estimated value range, market context, and a pricing recommendation with rationale — for a real-estate professional to review.
