---
name: model-selection-advisor
description: "Choose the right LLM for a task by trading off quality, cost, latency, and constraints. Use when asked which model to use, whether to upgrade/downgrade a model, how to cut LLM costs without hurting quality, or to justify a model choice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# model-selection-advisor

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

Produces a recommendation with the decision criteria, a per-option comparison, a routing strategy (cheap-by-default, escalate when needed), and how to validate the choice with an eval.
