---
name: treatment-plan-estimate
description: "Build a veterinary treatment plan with tiered options and a cost estimate to discuss with a pet owner. Use when asked to prepare a treatment plan, create an estimate for an owner, present diagnostic/treatment options, or have the cost conversation in a vet practice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# treatment-plan-estimate

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

Produces a clear plan (recommended vs. acceptable-alternative vs. minimum), line-item cost ranges, the medical rationale in plain language, and how to frame the money conversation with empathy so the owner can make an informed, unpressured decision.
