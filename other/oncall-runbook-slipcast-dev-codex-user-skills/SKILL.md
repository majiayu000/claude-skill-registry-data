---
name: oncall-runbook
description: "Write an on-call runbook for a service — covering alert definitions, escalation paths, common incident responses, and on-call handoff procedures. Use when asked to write an on-call guide, create alert runbooks, document escalation procedures, or prepare an on-call handoff document."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# oncall-runbook

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

Produces a structured on-call runbook with per-alert response procedures, escalation matrix, diagnostic commands, and handoff template.
