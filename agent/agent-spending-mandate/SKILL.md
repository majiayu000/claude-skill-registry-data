---
name: agent-spending-mandate
description: "Write a spending mandate that lets an AI agent buy things for you within strict limits: what it may buy, from whom, up to how much per purchase and in total, until when, and what needs your yes. Use when asked to let my agent make purchases, set a budget for an AI shopping agent, allow agentic checkout, limit what my assistant can spend, or prepare for agent payments."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-spending-mandate

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

Produces the mandate in plain words and as a structured block, the always-ask list and the review and revoke steps.
