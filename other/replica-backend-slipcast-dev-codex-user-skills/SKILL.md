---
name: replica-backend
description: 'Builds the backend of an app clone: auth, database migrations and access
  rules, payments with Stripe, email, background jobs and third-party integrations
  through official APIs only, plus a security checklist. Use when the user says "add
  login", "set up auth", "wire up the database", "add payments", "connect Stripe",
  "add Google Calendar", "send emails", "backend for my clone", or when /replica-build
  is running on fake data.'
metadata:
  source-package: replica-skill-main
  adapted-for: Codex
---

# replica-backend

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

