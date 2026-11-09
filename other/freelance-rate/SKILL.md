---
name: freelance-rate
description: "Derive a freelance day/hourly rate backwards from target income, honest billable utilization, overhead, and the self-employment tax premium — the arithmetic that proves a rate is not salary÷2000. Use when asked what should I charge as a freelancer, how do I set my consulting rate, why is my freelance rate so high, or convert my salary to a contract rate."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# freelance-rate

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

Produces the required-revenue breakdown, billable-hours math, the hourly and day rate, and the multiplier vs the naive salary÷2000 number.
