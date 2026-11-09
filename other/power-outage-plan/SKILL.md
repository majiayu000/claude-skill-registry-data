---
name: power-outage-plan
description: "Plan for an extended power outage — keeping medically-essential devices running, food safe, the home warm or cool enough, and communication alive — before the lights go out, with the special focus on power-dependent medical needs. Use when someone says 'prepare for a power outage', 'what if the power goes out for days', 'blackout plan', or 'I rely on a medical device that needs electricity'. Not medical advice; medical-device continuity routes to clinicians/utilities."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# power-outage-plan

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

Produces an outage plan tiered by duration, a medical-power priority plan, food/heat/cool/comms guidance, and safety warnings.
