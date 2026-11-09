---
name: clinical-research
description: Use when designing a prospective clinical study before submission — selecting
  and classifying endpoints (primary / key-secondary / exploratory, with surrogate-endpoint
  flagging), estimating sample size and power for two-arm designs (means / proportions
  / survival), or scoring a study plan for feasibility and a GO / GO-WITH-CONDITIONS
  / REDESIGN / NO-GO phase-gate decision. Every output is an ESTIMATE plus a named
  human owner (clinician / biostatistician / regulatory owner) — never clinical fact,
  never a finished protocol. Distinct from ra-qm-team, which handles the regulatory/QM
  submission (ISO 13485, EU MDR, FDA 510(k)/PMA/QSR), not the study design.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# clinical-research

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

