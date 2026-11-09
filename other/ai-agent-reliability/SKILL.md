---
name: ai-agent-reliability
description: "Make an AI agent or automation reliable enough to trust — the tests, checks, and guardrails that catch its failures before they reach anything real. Use when asked how do I test my AI agent, make my automation reliable, my agent works sometimes, or how do I trust an AI workflow in production."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-agent-reliability

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

Produces a map of where the agent can fail (bad input, hallucination, wrong tool call, edge cases, silent errors), the checks that catch each (validation, evals on real cases, human-in-the-loop gates, monitoring), a right-sized reliability plan scaled to the stakes, and a rollout that earns trust incrementally.
