---
name: action-runner
description: "Turn a skill's recommendations into real, executed actions — open the tickets, file the issues, post the updates — safely: dry-run preview, risk-classified, approval-gated, then recorded back to the brain. Use when asked to act on a plan, file tickets from a checklist, create issues from a PRD, execute the recommended next steps, or wire a skill's output into GitHub/Linear/Slack. Nothing acts silently."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# action-runner

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

## Требования к результату

Produces a dry-run actions plan with per-action risk, executes only after approval via the connected action MCP, and logs what was done.
