---
name: agent-era-pricing
description: "Redesign seat-based pricing for the agent era — when one human runs ten agents, per-seat models collapse. Use when agents are eroding seat counts, when asked to migrate to usage- or outcome-based pricing, to price an agent/API tier, or to defend revenue as customers automate their own usage. For general pricing and packaging strategy use pricing-strategy."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-era-pricing

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

Produces a pricing migration plan: the new value metric, fences, agent-tier design, cannibalisation math, and a phased migration for existing customers.
