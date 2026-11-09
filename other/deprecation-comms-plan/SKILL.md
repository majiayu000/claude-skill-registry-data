---
name: deprecation-comms-plan
description: "Plan the communications for deprecating a product, API, endpoint, or feature that customers depend on. Use when winding down or sunsetting something, planning a breaking change, or migrating customers off a legacy path. This is the customer-communications program — distinct from [[feature-sunset-plan]] (the kill decision, data handling, and code removal) and [[api-versioning-strategy]] (the technical versioning mechanics)."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# deprecation-comms-plan

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

Produces a staged timeline with grace periods, tiered customer messaging, a migration-guide outline, the channel plan, and an internal escalation playbook for the highest-risk accounts.
