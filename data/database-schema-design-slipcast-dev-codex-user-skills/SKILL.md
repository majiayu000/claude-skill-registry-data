---
name: database-schema-design
description: "Document or design a database schema with entity relationships, table definitions, constraints, indexes, and access patterns. Use when asked to design a database, document an existing schema, model entities and relationships, define table structures, plan an index strategy, or produce a data model for review."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# database-schema-design

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

Produces a structured schema document covering an ER diagram, table DDL definitions, index strategy, access pattern analysis, normalization decisions, and migration notes.
