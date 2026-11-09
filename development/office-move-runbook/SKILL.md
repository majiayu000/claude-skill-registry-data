---
name: office-move-runbook
description: "Run an office move or reconfiguration without losing a week of work — the dependency-ordered plan (internet lead times rule everything), the workstream owners, the comms that keep the team functional through the chaos, and the day-one-that-works checklist. Use when asked plan our office move, we're moving floors/buildings in six weeks, who owns what in the move, or make day one at the new office not a disaster."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# office-move-runbook

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

Produces the workstream map with owners, the dependency timeline, the team comms plan, and the day-one readiness gate.
