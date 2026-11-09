---
name: bug-report
description: "Write a clear, reproducible bug report that gets fixed fast. Use when asked to write a bug report, file a defect, report an issue, or turn 'it's broken' into an actionable ticket."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# bug-report

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

Produces a structured report — a precise title, steps to reproduce, expected vs. actual, environment, severity/priority, and evidence — so a developer can reproduce and fix it without a back-and-forth.
