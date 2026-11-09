---
name: spreadsheet-audit-live
description: Audit the user's REAL spreadsheet by opening it in the Cowork sandbox
  — not by reading a description of it. Use when asked to check this sheet before
  we present it, audit the model in my Drive, why don't these numbers add up, or is
  this spreadsheet safe to build on. Pulls the file via the Google Drive connector
  (or an uploaded .xlsx), opens it programmatically in the sandbox to trace formulas,
  hunts hardcodes / broken ranges / unit mixes, and produces a ranked findings artifact
  with a verified-vs-suspect ledger and a fix list.
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# spreadsheet-audit-live

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

