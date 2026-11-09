---
name: microservices-decomposition
description: "Design a microservices decomposition for a monolith or new system, defining service boundaries, ownership, communication patterns, and migration plan. Use when asked to decompose a monolith, define service boundaries, design a microservices architecture, or plan a strangler-fig migration."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# microservices-decomposition

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

Produces a bounded context map, service inventory table, communication pattern decisions, data ownership matrix, migration roadmap, and risk register.
