---
name: which-skill
description: "Route a fuzzy request to the right skill in this library. Use when the user is unsure which skill fits, asks 'which skill should I use for X', describes a task without naming a skill, or when a request could plausibly match several skills."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# which-skill

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

Produces a best-fit recommendation with the inputs to gather, a runner-up with the tie-breaker, and a workflow recipe when the job spans multiple skills.
