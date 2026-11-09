---
name: shared-agent-charter
description: "Write the charter for an AI agent a whole team shares (an OpenAI Dot in Slack or Teams, a shared Claude agent, a channel bot): who may give it instructions, which channels it works in, what it may say and do there, whose data it may read, who owns its mistakes, and how anyone can pause it. Use when asked to set rules for our team's agent, roll out Dots to my team, write a policy for a shared AI agent in Slack, decide who can instruct the bot, or govern an always-on agent across a team."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# shared-agent-charter

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

Produces a one-page charter to pin in the channel, an instruction-rights table, the data boundaries, the escalation and pause procedure, and the first-month review.
