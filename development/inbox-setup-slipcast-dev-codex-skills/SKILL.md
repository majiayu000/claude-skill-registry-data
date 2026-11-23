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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

