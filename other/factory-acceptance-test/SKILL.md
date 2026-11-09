---
name: factory-acceptance-test
description: "Write a factory acceptance test (FAT) plan or report — test coverage matrix against spec, AQL sampling plan, pass/fail criteria, golden-sample handling, deviation log, and sign-off structure. Use when asked to write a FAT plan, define outgoing quality inspection, set AQL levels, prepare for a factory acceptance or pre-shipment inspection, or document FAT results."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# factory-acceptance-test

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

Produces a complete FAT plan or report with sampling tables, defect classification, and a sign-off block.
