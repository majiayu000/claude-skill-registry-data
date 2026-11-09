---
name: business-operations-skills
description: Use when running, diagnosing, or designing internal business operations
  — process documentation, vendor SLAs, capacity planning, internal comms, SOP/runbook
  authoring, procurement spend. Triggers on "BizOps review", "where's the bottleneck",
  "vendor health", "internal SOP", "all-hands deck", "spend categorization", "capacity
  for Q3", "process mapping". Forks context to route to one of six BizOps sub-skills
  (process-mapper, vendor-management, capacity-planner, internal-comms, knowledge-ops,
  procurement-optimizer) and returns a digest. Distinct from business-growth (external
  sales motion) and c-level-advisor (strategic, not operational).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# business-operations-skills

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

