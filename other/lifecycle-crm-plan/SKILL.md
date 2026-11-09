---
name: lifecycle-crm-plan
description: "Design lifecycle marketing / CRM journeys across the customer lifecycle. Use when asked to plan onboarding emails, lifecycle/CRM campaigns, drip sequences, re-engagement or winback flows, or a messaging calendar."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# lifecycle-crm-plan

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

Produces a lifecycle plan — stage map, the trigger/message/goal for each journey, channel & timing, segmentation, suppression rules, and success metrics.
