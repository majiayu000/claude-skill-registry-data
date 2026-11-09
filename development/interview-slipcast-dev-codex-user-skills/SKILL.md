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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- В исходном наборе не разрешён ресурс ../../assets/. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
