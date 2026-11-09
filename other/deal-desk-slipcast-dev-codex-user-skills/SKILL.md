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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

