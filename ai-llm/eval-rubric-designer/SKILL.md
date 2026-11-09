---
name: eval-rubric-designer
description: "Design a scoring rubric and LLM-as-judge prompt to evaluate the quality of an AI feature's output. Use when asked to create an eval rubric, define quality dimensions, build an LLM judge, or decide how to measure whether AI output is good."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# eval-rubric-designer

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

Produces a rubric with weighted dimensions and concrete 1–5 anchors, a ready-to-run judge prompt, a labelling guide, and notes on judge reliability.
