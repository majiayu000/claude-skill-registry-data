---
name: epic-progress-report
description: "Report on an epic or initiative deeper than a status bullet — child work broken down by status, the riskiest unfinished pieces, and honest suggested cuts to hit the date. Use when asked for an epic progress report, where are we on this initiative, break down epic status, or what can we cut to ship on time."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# epic-progress-report

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

Produces the completion picture by child status, the critical-path and riskiest remaining work, a scope-cut menu with impact, and a straight call on whether the target date is realistic.
