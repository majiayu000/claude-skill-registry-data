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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

