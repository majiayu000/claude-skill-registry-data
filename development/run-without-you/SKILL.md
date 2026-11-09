---
name: run-without-you
description: Phase 4 of building a Claude Managed Agent — make it run without you.
  Turn a graded agent into a recurring scheduled deployment (POSIX-cron), an event-driven
  curl trigger, or confirmed on-demand use, then finalize the versioned roadmap. Use
  when the user says "run it every morning", "put it on a schedule", "nightly", "weekly",
  "automate this", "make it recurring", or when the orchestrator routes phase=run-without-you.
  deployment_builder.py builds the POST /v1/deployments payload (initial_events must
  include user.message; optionally nests a user.define_outcome so each firing self-grades);
  cron_validator.py validates the 5-field cron + IANA timezone and prints the wall-clock
  DST note; next_directions_writer.py writes NEXT-DIRECTIONS.md. No tool makes API
  calls — the deployment is created via BYOK curl. Distinct from grade-iterate (the
  in-session loop) and wrap-up (closeout).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# run-without-you

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

