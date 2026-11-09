---
name: late-invoice-escalation
description: "Collect overdue invoices with a graduated escalation ladder — friendly nudge to firm notice to work-stop to final demand, each with send-ready wording and timing, plus the prevention terms that stop the next one. Use when asked my client hasn't paid me, write a payment reminder email, invoice is 60 days overdue what do I do, or client is ghosting my invoices."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# late-invoice-escalation

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

Produces the situation read, the escalation ladder with dates and verbatim messages, the work-stop decision point, and the payment terms that prevent reruns.
