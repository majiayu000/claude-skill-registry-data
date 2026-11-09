---
name: agent-observability-spec
description: "Specify the tracing, metrics, and alerting for an AI agent or LLM feature in production. Use when asked what to log for an LLM app, design agent tracing or spans, define quality and cost monitors, or answer 'how do we know if the agent is misbehaving?'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-observability-spec

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

Produces an observability spec with a trace schema, metric definitions with owners and alert thresholds, sampling and retention policy, and a privacy note for logged content.
