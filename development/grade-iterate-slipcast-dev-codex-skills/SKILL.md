---
name: grade-iterate
description: Phase 3 of building a Claude Managed Agent — the bounded grade→iterate
  loop. Define a CMA outcome (a required markdown rubric graded by an isolated grader),
  read each verdict, decide the next move (sharpen / re-run / promote to schedule),
  and once a version passes, run held-back eval cases in parallel. Use when the user
  says "grade my agent", "make it pass the rubric", "iterate until it's good", "is
  it good enough", or when the orchestrator routes phase=grade-iterate. outcome_builder.py
  builds the user.define_outcome payload (rubric required, max_iterations clamped
  1..20 — never unbounded); verdict_reader.py reads the grader result and recommends
  the next move; eval_scaffold.py generates held-back cases + a parallel run plan
  (capped at the 25-thread CMA ceiling). Distinct from stage-launch (first launch)
  and run-without-you (scheduling).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# grade-iterate

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

