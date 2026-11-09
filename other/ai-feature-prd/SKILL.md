---
name: ai-feature-prd
description: "Write a PRD for an AI-powered feature, covering the things normal PRDs miss. Use when asked to spec an AI/LLM feature, write a PRD for a feature that uses a model, or plan an AI capability (assistant, summarizer, generator, classifier)."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-feature-prd

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

Produces an AI feature PRD — problem & UX of uncertainty, model approach, eval criteria, guardrails, fallback behaviour, the data flywheel, and cost/latency budget.
