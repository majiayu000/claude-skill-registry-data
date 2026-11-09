---
name: crypto-prices
description: "Fetch live cryptocurrency prices with zero API keys — CoinGecko's public endpoints primary, Coinbase spot fallback, via plain curl. Use when asked what's bitcoin at, ETH price in euros, how's the crypto market today, or price of some altcoin."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# crypto-prices

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

Produces the current price with 24h context, the source and timestamp, the rerunnable command, and the volatility caveat that crypto answers must carry.
