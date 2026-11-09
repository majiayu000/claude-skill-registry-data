---
name: ai-eval-plan
description: "Design an evaluation plan for an LLM or AI feature before shipping it. Use when asked how to evaluate a prompt/model/agent, set up an eval harness, define quality metrics for an AI feature, or build a regression gate."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-eval-plan

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

Produces an eval plan — task definition, datasets, metrics & rubrics, baselines, automated + human evals, a pass bar, and a regression gate.
