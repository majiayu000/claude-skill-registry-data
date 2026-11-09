---
name: invoice-generator
description: "Create a professional, complete invoice for a client or customer. Use when asked to write an invoice, create a bill, draft a freelance/contractor invoice, or set up an invoice template. Not tax/legal advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# invoice-generator

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

Produces a clear invoice — your and the client's details, a unique number, line items with quantities/rates, subtotal/tax/total, payment terms and methods, and due date — ready to send and easy to pay.
