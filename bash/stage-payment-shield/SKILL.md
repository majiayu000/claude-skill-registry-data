---
name: stage-payment-shield
description: "Set up deposits and stage payments that protect a tradesperson from the customer who won't pay AND read as fair to the customer — stage triggers tied to visible milestones, deposit sizing by job type, the payment terms paragraph for quotes, and the scripts for late stages. Use when a tradesperson asks 'how much deposit should I take', 'customer hasn't paid the second stage', 'payment terms for my quotes', or got burned on a big job."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# stage-payment-shield

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

Produces a stage-payment schedule, the terms paragraph, and firm-but-professional chase scripts.
