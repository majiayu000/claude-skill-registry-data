---
name: prompt-regression-suite
description: "Design a regression test suite that catches an LLM feature getting worse when the prompt, model, or context changes. Use when asked to stop prompt changes breaking production, set up golden tests or CI gates for an LLM feature, or test a model/prompt upgrade before shipping it. For designing first-time evaluation of a new feature use ai-eval-plan instead."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# prompt-regression-suite

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

Produces a golden case set, per-case pass criteria, CI gate thresholds, and a triage protocol for failures.
