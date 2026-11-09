---
name: warranty-claim
description: "Get a broken product repaired, replaced, or refunded under warranty — with the claim message written, the proof to attach, and the consumer-law backstop for when 'out of warranty' isn't the whole story. Use when asked to make a warranty claim, my [product] broke and it's still under warranty, the manufacturer won't honor the warranty, or how do I get this fixed for free."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# warranty-claim

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

Produces a ready-to-send claim message, the exact evidence to include, the repair-vs-replace-vs-refund position, and an escalation ladder for when the first answer is no.
