---
name: inbox-setup
description: 'One-time setup skill that builds a personalized inbox triage knowledge
  base via interactive interview. Interviews the user about their email patterns,
  business context, reply style, and priorities using grill-me discipline (one question
  at a time, forcing format where possible, dependency-ordered, each question explains
  why I''m asking), then generates the knowledge base files that power the companion
  ''inbox-triage'' skill. Run this once before using inbox-triage for the first time.
  Re-run when business, pricing, or priorities change significantly. Triggers: ''set
  up my inbox'', ''configure inbox triage'', ''set up my email system'', ''configure
  email triage'', ''build my email knowledge base'', ''initialize email management'',
  ''set up inbox triage'', ''onboard email triage'', or any variation where someone
  wants to get the email triage system running for the first time.'
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# inbox-setup

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

