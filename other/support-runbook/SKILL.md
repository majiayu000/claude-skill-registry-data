---
name: support-runbook
description: "Write a support runbook for handling a recurring issue type consistently. Use when asked to write a support runbook, a troubleshooting playbook for agents, a handling guide for a common issue, or a tier-1 response procedure."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# support-runbook

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

Produces a runbook — issue identification, triage/severity, step-by-step diagnosis & resolution, decision tree, when/how to escalate, and the customer-comms templates — so any agent resolves it the same way.
