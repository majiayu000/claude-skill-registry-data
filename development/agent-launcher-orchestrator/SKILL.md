---
name: agent-launcher-orchestrator
description: Use when a user wants to build, launch, grade, or schedule a Claude Managed
  Agent (CMA) in their own Anthropic account — "build me an agent", "launch this as
  a managed agent", "run this on a schedule", "grade my agent against a rubric", "set
  up a nightly worker". Reads the per-session goal (./my-agent/goal.json), routes
  deterministically to one of five phase sub-skills (interview → stage-launch → grade-iterate
  → run-without-you → wrap-up) via goal_router.py, and compiles the goal+phase into
  an execution shape (single-pass workflow / bounded grade→iterate loop / recurring
  cron deployment loop) via loop_compiler.py. Forks context so heavy intake (build
  sheets, payloads, eval cases) stays out of the parent thread. All launches are emitted
  as BYOK curl the user runs with their own key; no tool makes API calls. Inspired
  by anthropics/launch-your-agent (Apache-2.0).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# agent-launcher-orchestrator

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

- В исходном наборе не разрешён ресурс ../../references/. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
