---
name: home-contractor-quote-decoder
description: "Decode a home renovation or repair quote — allowances that aren't prices, exclusions that become change orders, payment schedules that shift risk, and what a comparable-bids check should cover. Use when someone asks 'is this contractor quote fair', 'decode this renovation bid', 'what should be in a contractor contract', or 'why do these three bids differ so much'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# home-contractor-quote-decoder

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

Produces a section-by-section decode, the allowance and exclusion audit, payment-schedule risk analysis, and the questions that make bids comparable.
