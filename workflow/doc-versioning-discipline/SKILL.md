---
name: doc-versioning-discipline
description: "Keep living documents trustworthy over time — the status header (draft/active/superseded) that tells readers what they're holding, the change-log-for-decisions inside the doc, the supersession chain that kills zombie versions, and the review-date heartbeat. Use when asked which version of this doc is current, our wiki is full of stale pages, set up doc lifecycle rules, or people keep following the old process doc."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# doc-versioning-discipline

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

Produces the status-header standard, the in-doc change log, the supersession protocol, and the staleness heartbeat.
