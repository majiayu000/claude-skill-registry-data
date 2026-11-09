---
name: spreadsheet-handover
description: "Hand over a spreadsheet so it survives its author leaving — the README tab that decodes the sheet's logic, the update runbook with sources and cadence, the fragility warnings, and the walkthrough that transfers the judgment. Use when asked document this spreadsheet before I leave, hand over the model to the team, make this sheet survivable without me, or we inherited a workbook nobody understands."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# spreadsheet-handover

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

Produces the README tab content, the update runbook, the known-fragilities list, and the handover walkthrough agenda.
