---
name: knowledge-ops
description: Use when a Head of Ops, Knowledge Manager, or TPM-Internal needs to author,
  validate, or clean up company SOPs and internal runbooks (procurement intake, vendor
  offboarding, incident-comms cascade, employee onboarding) — including 5W2H completeness
  checks (Who-What-When-Where-Why-How-HowMuch), cross-link and orphan-page validation
  across a sprawling Notion/Confluence/Obsidian wiki, KB ingestion + hygiene reporting,
  and runbook step verification (named owner, expected duration, observable success
  signal, rollback path, escalation contact). Pairs Ishikawa's 5W2H method, Gawande's
  *The Checklist Manifesto*, ISO 9001, ITIL v4, and Google SRE Workbook runbook discipline
  with deterministic stdlib-only Python tools that score completeness, detect anti-patterns,
  and emit prioritized cleanup lists (e.g., "validate this runbook before it goes
  into rotation", "audit our Confluence wiki for stale and orphaned SOPs").
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# knowledge-ops

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

