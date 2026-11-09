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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

