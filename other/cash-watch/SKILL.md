---
name: cash-watch
description: "Set up a proactive agent to watch a small business's cash every day across Stripe, QuickBooks or Xero and the bank feed: today's cash position, money due in and out this week, failed payments, new disputes and the runway line, with clear rules for what interrupts you and what waits for the morning brief. Use when asked to have my agent keep an eye on cash, daily cash check for Duet, alert me about failed payments or disputes, watch my runway, or monitor Stripe and QuickBooks for me."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cash-watch

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

Produces the watch definition (sources, checks, thresholds), the interrupt and brief rules, the daily cash lines in a fixed format, and the drafts the agent may prepare.
