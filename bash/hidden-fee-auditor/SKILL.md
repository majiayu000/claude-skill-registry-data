---
name: hidden-fee-auditor
description: "Scan a bill, contract, or quote for junk and hidden fees — the padding buried in the fine print — and get them questioned or removed. Use when asked to check this bill for hidden fees, are these charges legit, what am I actually paying for, or review this quote for junk fees."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# hidden-fee-auditor

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

Produces a line-by-line read flagging suspicious/vague/padded charges, which are commonly negotiable or bogus, the questions to ask and script to dispute them, and an estimate of what you could save — across bills like telecom, hotels, cars, banking, and services.
