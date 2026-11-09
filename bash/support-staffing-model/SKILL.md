---
name: support-staffing-model
description: "How many support agents does the queue actually need — Erlang C, computed, not 'tickets per agent' folklore. Use when staffing a support/CS team, defending headcount, or checking whether an SLA is mathematically possible with the current roster."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# support-staffing-model

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

Produces agent counts across load scenarios (with shrinkage), occupancy and average-wait numbers, and a real .xlsx — via the bundled zero-dependency script.
