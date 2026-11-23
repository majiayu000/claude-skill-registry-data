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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- В исходном наборе не разрешён ресурс ../../references/. Не считай его прочитанным; используй доступные материалы и явно укажи ограничение, если он необходим задаче.
