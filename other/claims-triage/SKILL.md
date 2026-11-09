---
name: claims-triage
description: "Triage an incoming insurance claim: check the coverage trigger against policy wording, band severity and complexity, screen for fraud indicators, set a first-pass reserve range, and route with an SLA. Use when asked to triage a claim, review a first notice of loss (FNOL), assess a new claim, decide fast-track vs adjuster routing, or screen a claim for SIU referral."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# claims-triage

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

Produces a structured triage note with coverage view, severity band, indicator screen, reserve range, and a routing recommendation.
