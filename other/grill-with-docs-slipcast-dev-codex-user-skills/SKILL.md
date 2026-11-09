---
name: grill-with-docs
description: Docs-anchored grilling session — challenges a plan against the project's
  existing language (CONTEXT.md) and recorded decisions (docs/adr/), and updates those
  files inline as terminology and decisions crystallise. Use when user wants to stress-test
  a plan against documented domain language, or mentions "grill with docs".
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# grill-with-docs

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

