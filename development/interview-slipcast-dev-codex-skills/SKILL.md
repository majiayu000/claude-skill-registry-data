---
name: interview
description: Phase 1 of building a Claude Managed Agent — interview the founder about
  the one job the agent should do, then produce a build sheet (CMA primitives table
  + v1/v2 deferrals + eval plan) WITHOUT needing their API key yet. Use when the user
  says "help me scope an agent", "I have an idea for an agent", "what should this
  agent be", or when the orchestrator routes phase=interview. Drives the six intake
  slots (job, trigger, inputs, actions, definition-of-done, recurrence) via AskUserQuestion,
  maps them to primitives with interview_planner.py, assembles build-sheet.json with
  build_sheet_builder.py, and validates limits with primitives_validator.py. Connectors
  are mockable in v0 (schema-true custom tools); real MCP servers become v1 deferrals.
  Distinct from stage-launch (which turns the sheet into payloads).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# interview

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- В исходном наборе не разрешён ресурс ../../assets/. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
