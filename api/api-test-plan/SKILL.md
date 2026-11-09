---
name: api-test-plan
description: "Plan tests for an API endpoint or service — functional, negative, and contract. Use when asked to test an API, write API test cases, plan REST/GraphQL endpoint testing, or validate an API contract."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# api-test-plan

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

Produces an API test plan — per-endpoint cases (status codes, schema, auth, validation, errors), boundary/negative cases, contract checks, and non-functional notes — so the API is verified beyond the happy 200.
