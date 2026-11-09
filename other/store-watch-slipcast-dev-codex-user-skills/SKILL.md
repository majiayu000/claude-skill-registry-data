---
name: store-watch
description: "Have a proactive agent watch an online shop (Shopify, WooCommerce, Etsy) for what needs the owner: best-sellers about to run out, a spike in refunds or returns on one product, bad reviews, failed orders and checkout problems, with interrupts only for what cannot wait and drafted replies for reviews. Use when asked to monitor my Shopify store, have Duet watch my shop, alert me when stock runs low, watch for bad reviews, or daily store health check."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# store-watch

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

Produces the watch rules, the daily store lines, the interrupt thresholds, and drafted review replies; it never changes prices, refunds orders or publishes anything.
