---
name: collections-email
description: "Write a polite-but-firm payment-reminder / collections email sequence for overdue invoices. Use when asked to write a collections email, a payment reminder, a dunning sequence, or to chase an overdue invoice. Not legal advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# collections-email

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

Produces a staged sequence — gentle pre-due nudge through escalating overdue reminders to a final notice — that stays professional, keeps the relationship intact, and makes paying easy.
