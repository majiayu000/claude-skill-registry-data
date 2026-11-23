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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

