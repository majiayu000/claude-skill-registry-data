---
name: replica-architect
description: Plans the stack, database schema and API for an app clone, from the recon
  map replica-recon wrote. Picks boring, managed tech, turns the inferred data model
  into real SQL with indexes and access rules, lists every route by flow, and orders
  the build as a thin vertical slice first. Use when the user says "plan the clone",
  "what stack should I use", "design the database", "write the schema", "plan the
  API", "architecture for my version of X", or after /replica-recon finishes.
metadata:
  source-package: replica-skill-main
  adapted-for: Codex
---

# replica-architect

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

