---
name: winback-playbook
description: "Turn an at-risk or churned account into a save play — root-cause hypothesis, the offer ladder, the outreach sequence, and the honest call on when to let go. Use when asked to save a churning customer, build a win-back plan, re-engage a lost account, or stop a renewal from slipping."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# winback-playbook

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

Produces the churn diagnosis, a ranked set of save levers, a timed outreach sequence, and the walk-away line so you don't over-invest in an account that's gone.
