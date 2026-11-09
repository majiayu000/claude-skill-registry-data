---
name: dental-clinical-note
description: "Write a dental chart note that survives an insurance audit, a recall years later, and a colleague picking up the case cold — the finding, the justification, the consent conversation, and the materials, in the order a reviewer looks for them. Use when asked to write a chart note, document a procedure, improve clinical documentation, or when a claim was denied for insufficient documentation. Documentation support only; the clinical content is the treating clinician's."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# dental-clinical-note

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

Produces a structured note with subjective, objective, assessment and plan, the medical necessity justification, consent documented, materials and lot numbers, and the next-visit plan.
