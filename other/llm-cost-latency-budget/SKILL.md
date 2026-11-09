---
name: llm-cost-latency-budget
description: "Model the cost and latency of an LLM feature before it ships and surprises the bill. Use when asked to estimate LLM API costs, set a latency/token budget, decide which model tier to use, or bring down the cost of an AI feature."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# llm-cost-latency-budget

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

Produces a cost & latency budget — token math per request, monthly cost projection, model tiering, caching/streaming levers, p95 latency targets, and a guardrail/alert plan.
