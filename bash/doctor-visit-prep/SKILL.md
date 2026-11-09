---
name: doctor-visit-prep
description: "Prepare for a doctor's appointment so the 12 minutes actually get used — the symptom timeline in the format clinicians think in, the prioritized question list, and the advocacy scripts for being heard. Use when asked help me prepare for my doctor appointment, what should I tell my doctor, organize my symptoms, or I always forget what to ask."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# doctor-visit-prep

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

Produces the one-page visit sheet: symptom history with timeline, medications, the top-3 questions, and the phrases that get concerns taken seriously.
