---
name: kyc-escalation
description: "Write an internal KYC/AML escalation memo: a factual time-stamped trigger description, customer-profile vs activity mismatch analysis, red-flag taxonomy mapping, outstanding information, and a recommendation with rationale. Use when asked to escalate a KYC alert, document an AML concern, write up unusual-activity findings for compliance review, or prepare an enhanced due diligence referral."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# kyc-escalation

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

Produces a structured internal escalation memo for a compliance team's decision-makers.
