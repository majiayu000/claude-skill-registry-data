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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

