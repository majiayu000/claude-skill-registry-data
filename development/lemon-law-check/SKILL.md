---
name: lemon-law-check
description: "Figure out whether your problem car might qualify for a refund or replacement under lemon law or warranty — and build the paper trail to claim it. Use when asked is my car a lemon, my new car keeps breaking, lemon law help, or can I return a defective car. Not legal advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# lemon-law-check

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

Produces a plausibility read against typical lemon-law criteria (repeated same defect, repair attempts, time out of service, warranty window), the records to gather, the manufacturer-claim and escalation steps, and a strong flag that lemon laws are jurisdiction-specific.
