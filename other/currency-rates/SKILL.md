---
name: currency-rates
description: "Convert currencies and fetch live exchange rates with zero API keys — Frankfurter (ECB rates) primary, open.er-api.com fallback, via plain curl. Use when asked convert 500 dollars to euros, what's the USD-INR rate, how much is this in my currency, or historical exchange rate for a date."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# currency-rates

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

Produces the conversion with the rate and its date quoted, the rerunnable command, and the not-a-trading-quote caveat.
