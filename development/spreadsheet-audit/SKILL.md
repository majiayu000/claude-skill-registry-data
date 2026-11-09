---
name: spreadsheet-audit
description: "Audit a spreadsheet before trusting it — the error hunt (hardcoded overrides, broken ranges, silent unit mixes), the fragility map (what breaks when rows are added), and the load-bearing-formula review that catches the mistake before the meeting does. Use when asked check this spreadsheet before we present it, why don't these numbers add up, audit this model someone left behind, or is this sheet safe to build on."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# spreadsheet-audit

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

Produces the findings ranked by damage, the fragility map, the verified-vs-suspect ledger, and the fix list.
