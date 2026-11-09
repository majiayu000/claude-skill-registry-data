---
name: process-mapper
description: Use when a BizOps lead, COO, or process-improvement owner needs to document
  an end-to-end business process (procurement, employee onboarding, incident handoff,
  customer-onboarding, claims adjudication) in BPMN-style notation, measure cycle
  times by stage, surface where work spends most of its time waiting vs. being worked,
  and quantify the gap between processing time and total elapsed time. Pairs Lean
  / Six Sigma / Theory-of-Constraints canon with deterministic stdlib-only Python
  tools to produce a process map, a ranked bottleneck list (with severity + root-cause
  hypothesis), and a cycle-time analysis (P50, P90, value-add ratio, Little's-Law
  throughput). Distinct from sales-pipeline, system-reliability (SLO), and strategic-OKR
  work — this is tactical process documentation for internal operations.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# process-mapper

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

