---
name: run-an-agent-team
description: "Design a small team of AI agents to tackle a complex task in parallel — who does what, how they hand off, and how to keep them coordinated — instead of one overloaded agent doing everything serially. Use when asked how do I use multiple AI agents, set up an agent team, orchestrate agents for, or run agents in parallel."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# run-an-agent-team

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

Produces a decomposition of the task into agent roles, a coordination pattern (parallel vs sequential, how outputs combine), the context each agent needs (and what to keep isolated), a review/quality step, and the guardrails to keep it from going off the rails — practical multi-agent design for real tasks.
