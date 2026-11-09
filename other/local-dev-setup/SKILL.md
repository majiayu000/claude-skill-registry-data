---
name: local-dev-setup
description: "Write a local development environment setup guide for a service or project — covering prerequisites, repository setup, environment variables, local service dependencies, database seeding, running the service, running tests, common gotchas, IDE recommendations, and first-contribution checklist. Use when asked to write a dev setup guide, create onboarding documentation for engineers, document local environment setup, or write a getting-started guide for a codebase."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# local-dev-setup

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

Produces a complete setup guide that a new engineer can follow from zero to running tests in under 30 minutes, with a troubleshooting section for the most common setup failures.
