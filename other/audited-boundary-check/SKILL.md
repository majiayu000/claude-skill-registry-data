---
name: audited-boundary-check
description: "Use when asked to check whether a figure is audited, which headline numbers sit outside the audited accounts, what 'adjusted' or 'underlying' means in this report, or who is vouching for the numbers in the highlights. For every headline figure in the highlights, chairman's statement and CEO review of an uploaded annual report, states whether it sits inside or outside the audited statements and what was added or removed versus the nearest audited number. Educational, not financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# audited-boundary-check

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

Produces a boundary table, the list of figures outside the boundary, and a plain-English summary of who is vouching for what.
