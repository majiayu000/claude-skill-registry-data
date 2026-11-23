---
name: deal-desk
description: Use when reviewing a specific inbound deal before close — when sales
  has asked for a discount that exceeds AE authority, when the customer has redlined
  the MSA, when per-deal economics (margin after discount, multi-year payment shape,
  indemnity exposure) need to be quantified, or when discount approval needs to be
  routed to a named human approver (Sales Director, VP Sales, CFO, CRO, General Counsel).
  Covers deal review, discount approval routing, per-deal margin scoring, deal exception
  handling, MSA redline triage, contract landmine detection (uncapped indemnity, MFN,
  perpetual license-back, missing DPA), and named-approver chain assembly. NEVER auto-approves
  — every output is a numeric scorecard plus a routing recommendation to a named human.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# deal-desk

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

