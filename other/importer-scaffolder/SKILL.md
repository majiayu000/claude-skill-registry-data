---
name: importer-scaffolder
description: Use when asked to build an importer from a competitor's export, migrate
  users' data from another tool, map a CSV or JSON export onto my data model, or make
  switching to my project easy. Given a sample export (CSV or JSON), produces a field
  mapping table, an importer code skeleton, a rule that unmatched records are kept
  rather than dropped, and test fixtures including the awkward cases. For a database
  migration inside one system, use database-migration-plan.
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# importer-scaffolder

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

