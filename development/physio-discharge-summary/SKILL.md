---
name: physio-discharge-summary
description: "Write a physiotherapy discharge summary that closes the episode properly — outcomes against the goals that were set, what the patient is leaving with, what would bring them back, and what the referrer actually needs to know. Use when asked to write a discharge summary, close an episode of care, write to a referrer at discharge, or discharge a patient who has not fully recovered. A documentation framework for a licensed clinician."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# physio-discharge-summary

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

Produces the outcome summary against baseline, the self-management plan, the flare-up and return criteria, the referrer letter, and the record of incomplete goals.
