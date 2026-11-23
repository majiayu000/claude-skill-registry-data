---
name: agent-regression-evals
description: Use when an agent, prompt, model or tool change needs proof it did not
  make the agent worse — setting up a regression eval suite, deciding whether a pass-rate
  drop is real or noise, grading tool-call trajectories, finding flaky eval cases,
  or wiring an eval gate into CI that blocks the merge. Runs repeated trials, reports
  pass@k and pass^k, compares candidate to baseline with paired statistics, and refuses
  to pass a dropped case, a critical-case regression, or a forbidden tool call.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# agent-regression-evals

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

