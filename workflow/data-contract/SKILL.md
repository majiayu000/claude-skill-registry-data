---
name: data-contract
description: "Define a data contract between a producer and consumers of a dataset/event/API. Use when asked to write a data contract, define a schema agreement, set data SLAs, or stop a producer from silently breaking downstream consumers."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# data-contract

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

Produces a contract — schema with types & constraints, semantics, quality SLAs (freshness/completeness/validity), ownership, versioning & breaking-change policy, and a change process.
