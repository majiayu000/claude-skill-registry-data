---
name: qa-release-signoff
description: "Produce a QA release sign-off / go-no-go readiness report. Use when asked for a release sign-off, a go/no-go QA report, release readiness, or a test summary before shipping."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# qa-release-signoff

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

Produces a sign-off — what was tested and the results, open defects by severity, coverage and residual risk, the go/no-go recommendation with conditions, and a rollback note — so the release decision is evidence-based, not a vibe.
