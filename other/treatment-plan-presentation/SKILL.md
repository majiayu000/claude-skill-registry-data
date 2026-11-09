---
name: treatment-plan-presentation
description: "Present a dental treatment plan the patient actually understands and accepts — sequenced by clinical priority, costed with their coverage applied, and explained in the order that answers what-is-wrong before what-it-costs. Use when asked to present a treatment plan, improve case acceptance, explain treatment to a patient, or handle a patient who says they want to think about it. Clinical decisions remain the treating clinician's; this shapes the conversation, not the diagnosis."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# treatment-plan-presentation

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

Produces the phased plan, the plain-language explanation per phase, the cost and coverage breakdown, the consequences-of-delay framing, and responses to the four common objections.
