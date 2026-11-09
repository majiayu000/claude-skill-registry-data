---
name: discharge-summary
description: "Turn a hospital stay into a complete, well-structured discharge summary. Use when asked to write a discharge summary, a hospital discharge note, or to document a patient's admission-to-discharge course for handoff."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# discharge-summary

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

Produces a standard discharge summary — admission reason, hospital course, diagnoses, procedures, discharge medications, condition, and follow-up/return precautions — from the provided details.
