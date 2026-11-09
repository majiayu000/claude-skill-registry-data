---
name: pricing-calculator
description: "Model pricing scenarios — tiers, margins, break-even, and the revenue impact of a price change. Use when asked to calculate pricing, model a price increase, find break-even volume, set tier prices to a margin target, or estimate the revenue effect of a pricing change."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# pricing-calculator

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

Produces a computed pricing model (per-tier margin, break-even units, price-change revenue impact with an elasticity assumption) and a recommendation.
