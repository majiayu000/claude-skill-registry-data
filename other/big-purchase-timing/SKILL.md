---
name: big-purchase-timing
description: "Decide when to buy a big-ticket item to get the best price — the sales cycles, model-refresh timing, and 'buy now vs wait' math for the specific thing you want. Use when asked when's the best time to buy [item], should I wait for a sale, is now a good time to buy, or when do [products] go on sale."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# big-purchase-timing

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

Produces the typical discount calendar for that category, whether a new model/version is due (and if the current one will drop), a buy-now-vs-wait recommendation for your timeline, and price-tracking tactics — flagging that timing is a guide, not a guarantee.
