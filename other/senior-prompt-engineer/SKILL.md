---
name: senior-prompt-engineer
description: Use when the user asks to optimize prompts, design prompt templates,
  evaluate LLM outputs with an eval set, measure RAG retrieval quality, validate agent/tool
  configurations, analyze token usage, or design structured-output contracts. Covers
  eval-driven prompt iteration, RAG metrics (relevance, faithfulness, coverage), agent
  workflow validation, and token/cost budgeting — all model-agnostic, with three stdlib
  Python tools.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# senior-prompt-engineer

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
