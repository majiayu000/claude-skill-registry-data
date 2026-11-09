---
name: hipaa-safeguards
description: "Map HIPAA Security Rule safeguards and run a risk analysis for systems handling PHI. Use when asked to become HIPAA-compliant, assess HIPAA safeguards, prepare for handling PHI/ePHI, or scope a BAA."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# hipaa-safeguards

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

Produces a HIPAA assessment — the administrative/physical/technical safeguards with required-vs-addressable status, a risk analysis, BAA scope, and a prioritised remediation plan.
