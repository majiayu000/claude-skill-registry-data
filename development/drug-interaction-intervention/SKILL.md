---
name: drug-interaction-intervention
description: "Document a pharmacist's clinical intervention — the interaction or error spotted, what was done, what the prescriber decided, and the outcome — so the record shows the catch and the care that followed. Use when asked to document a clinical intervention, record a prescriber call about an interaction, log a near-miss, or build an intervention record for audit or remuneration. A documentation framework for a licensed pharmacist; every interaction and severity judgement must be verified against current references."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# drug-interaction-intervention

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

Produces the intervention record with severity and evidence, the prescriber-call script, the outcome and follow-up, and the aggregate reporting fields.
