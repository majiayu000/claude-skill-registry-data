---
name: policy-memo
description: "Write a decision-ready policy memo that frames an issue and recommends an option. Use when asked to write a policy memo, options paper, decision memo for a principal/minister/executive, or brief a decision-maker on a policy choice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# policy-memo

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

Produces a tight memo: the issue, background, options with trade-offs, a clear recommendation, and implementation/risks — written for a busy decision-maker who reads the first paragraph.
