---
name: stock-snapshot
description: "Fetch a stock quote snapshot with keyless curl — Yahoo Finance's public chart endpoint, read with the discipline unofficial market data demands: timestamped, delayed-flagged, and never advice. Use when asked what's this stock at, how did the market do today, get me a ticker's recent range, or pull basic price history."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# stock-snapshot

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

Produces the quote with change and range context, the source-honesty caveats (unofficial, possibly delayed), the rerunnable command, and a hard no-advice line.
