---
name: cn-trade-quotation
description: "Use when asked 做一份外贸报价单, FOB 和 CIF 怎么报价, 出口报价核算, 报价怎么算利润, 退税怎么算进报价, quotation sheet for an export order, or price an export quotation from China."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-trade-quotation

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

Produces a cost build-up from the factory price through export tax rebate, domestic logistics, port charges, freight and insurance to each Incoterms 2020 term, a quotation sheet in English with a Chinese summary, quantity tiers, validity and exchange-rate assumptions, payment terms and the risk each term puts on the seller, with rates marked to confirm.
