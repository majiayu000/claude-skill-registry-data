---
name: human-in-the-loop-design
description: "Design the human approval surface for an agent system — which actions gate, how approvals batch without becoming rubber stamps, and what the audit trail must hold. Use when asked to add human oversight to an agent, design approval workflows for AI actions, decide what an agent may do autonomously, or fix approval fatigue in an existing loop. For specifying the whole agent use agent-spec; for the per-skill execution gates see the Execution-block pattern in SKILLSPEC §5."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# human-in-the-loop-design

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

Produces an action-tier policy, approval UX spec, escalation rules, and audit-trail requirements.
