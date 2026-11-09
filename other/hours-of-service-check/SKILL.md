---
name: hours-of-service-check
description: "Audit driver hours records for the violations that actually get cited — the falsification patterns, the edit trails, and the scheduling that makes compliance impossible — and fix the causes rather than the logs. Use when asked to audit hours of service, review driver logs, check tachograph or ELD records, prepare for an hours compliance review, or reduce hours violations. Rules and limits are jurisdiction-specific and must be verified against current regulation."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# hours-of-service-check

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

Produces the violation summary by type and severity, the falsification-pattern review, the scheduling root-cause analysis, the driver-level and systemic actions, and the audit trail.
