---
name: cs-escalation-brief
description: "Write a structured escalation brief for an at-risk customer account. Use when an account has escalated, when a customer is threatening churn, when a P1 customer issue needs executive attention, or when preparing an internal save play."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cs-escalation-brief

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

Produces a crisp escalation brief with account context, timeline, root cause, business impact, and a clear resolution plan.
