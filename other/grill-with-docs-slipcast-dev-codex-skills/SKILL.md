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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

