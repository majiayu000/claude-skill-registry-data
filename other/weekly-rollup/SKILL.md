---
name: weekly-rollup
description: "Roll a week of daily reports and agent activity into one honest weekly summary: trajectory against goals, what shipped with proof, the recurring blocker, and what to change next week. Use when asked for a weekly rollup, summarise my week, what did the agent accomplish this week, or a Friday wrap-up from my daily reports."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# weekly-rollup

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

Produces a 12-line weekly rollup in the shared status vocabulary: shipped versus planned, the pattern in the blockers, and one concrete change for next week.
