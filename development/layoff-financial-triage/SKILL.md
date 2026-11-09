---
name: layoff-financial-triage
description: "The first-72-hours money plan after a layoff — runway computed, deadlines caught, bleeding stopped, in priority order. Use when asked I just got laid off what do I do about money, build my layoff budget, how long can I last, or what needs to happen this week."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# layoff-financial-triage

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

Produces the runway number, the deadline list (healthcare, unemployment filing, equity exercise windows), the spending triage, and a one-week action checklist.
