---
name: excel-model
description: "Build a real, formula-driven Excel (.xlsx) model — not a static table. Use when asked to build an Excel model, a financial model, a budget/forecast spreadsheet, or any .xlsx with live formulas a user can edit. Requires a code-execution environment (Claude Code, the API code tool, or Claude.ai)."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# excel-model

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

Produces an actual .xlsx file via a generated openpyxl script: an inputs/assumptions sheet, calculation sheets with real cell formulas, and formatting — so changing an input recalculates the model.
