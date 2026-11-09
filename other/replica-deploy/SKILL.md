---
name: replica-deploy
description: 'Ships an app clone live on the user''s own domain: a preflight gate
  (tests green, parity must-haves done, rebrand sweep clean, listing linted, legal
  pages up), production database and env vars, the host, DNS records for the domain
  and for email, Stripe live mode, OAuth redirects, monitoring, and mobile builds
  to TestFlight and Play. Use when the user says "deploy it", "ship it", "put it live",
  "connect my domain", "go to production", "publish the app", or after /replica-launch.'
metadata:
  source-package: replica-skill-main
  adapted-for: Codex
---

# replica-deploy

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
