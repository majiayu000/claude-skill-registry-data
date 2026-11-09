---
name: bug-diagnosis
description: "Diagnose a bug systematically instead of guessing — reproduce, isolate, form hypotheses, and test them to root cause. Use when debugging, chasing a defect, an intermittent failure, or 'why is this happening?'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# bug-diagnosis

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

Produces a structured diagnosis: a reliable repro, the narrowed-down location, ranked hypotheses with how to test each, and the root cause + fix once found.
