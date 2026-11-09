---
name: product-recall-check
description: "Find out whether something you own — a car, appliance, car seat, food item, or gadget — is under a safety recall, and what to do about it. Use when asked to check for a recall, is my [product] recalled, I heard about a recall on, or how do I find out if my car/appliance is affected."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# product-recall-check

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

Produces a structured way to check by make/model/batch against the official sources, how to read whether your specific unit is affected, the free remedy you're owed, urgency triage for safety risks, and how to register for future recall alerts — flagging that you must confirm against the current official database.
