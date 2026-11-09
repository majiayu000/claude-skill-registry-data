---
name: database-migration-plan
description: "Write a safe, zero-downtime database migration plan for a schema change. Use when asked to plan a database migration, design a zero-downtime schema change, document an expand/contract migration, produce a rollback procedure for a database change, or coordinate a database schema update with a deployment."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# database-migration-plan

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

Produces a structured migration plan covering migration objectives, backward compatibility analysis, expand/contract phase breakdown, exact SQL, rollback steps per phase, data validation queries, and a deployment runbook.
