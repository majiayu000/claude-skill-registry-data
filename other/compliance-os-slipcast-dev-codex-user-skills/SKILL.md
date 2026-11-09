---
name: compliance-os
description: 'Compliance OS — meta-orchestrator that lets compliance teams CONFIGURE
  which frameworks apply, COMPUTE cross-framework control overlap, SIMULATE internal
  audits, and CONSOLIDATE evidence across multiple frameworks. Four decisions: (1)
  Given a company profile, which of the 12 supported frameworks apply (ISO 27001/13485/42001/14971,
  EU AI Act, MDR 745, GDPR, SOC 2, FDA QSR, NIST CSF 2.0, NIS2, HIPAA)? (2) Across
  selected frameworks, which controls overlap and how much evidence reuses? (3) For
  a given framework + scope, what does a realistic mock audit produce — drawing from
  the 205-scenario library? (4) Across selected frameworks, what''s the unified evidence
  checklist with reuse map? Use when standing up a multi-framework program, planning
  the annual audit calendar, or preparing for certification stage 1. Does NOT replace
  per-framework skills (it orchestrates them).'
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# compliance-os

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
