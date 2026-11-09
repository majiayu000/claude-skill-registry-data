---
name: late-invoice-chaser
description: "Chase an overdue invoice and actually get paid — a firm-but-friendly escalation ladder that protects the client relationship until it's clear the relationship is the problem. Use when asked to chase an unpaid invoice, my client hasn't paid, write a payment reminder, or how do I get a late-paying client to pay."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# late-invoice-chaser

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

Produces a staged sequence of messages (gentle nudge → firm reminder → final notice → next steps) timed to the overdue days, with late-fee and work-pause options and a note on what to keep for the record.
