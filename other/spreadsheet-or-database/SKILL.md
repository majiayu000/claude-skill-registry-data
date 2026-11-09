---
name: spreadsheet-or-database
description: "Decide honestly when a spreadsheet should become a database or app — the five outgrowth signals (concurrent editing, relational strain, permission needs, scale, process-in-comments), what staying costs vs what migrating costs, and the incremental escape paths. Use when asked should this be a database, our spreadsheet is breaking, is it time to move off sheets, or what should replace this monster workbook."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# spreadsheet-or-database

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

Produces the signal assessment on the actual workbook, the stay-vs-move verdict with costs both ways, and the migration path sized to the team.
