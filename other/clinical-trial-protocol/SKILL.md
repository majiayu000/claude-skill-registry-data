---
name: clinical-trial-protocol
description: "Draft a clinical trial protocol synopsis with the elements regulators and IRBs expect. Use when asked to write a clinical trial protocol, a study protocol synopsis, a trial design, or to structure endpoints/eligibility/statistics for an interventional study."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# clinical-trial-protocol

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

Produces a structured protocol synopsis — objectives, design, population with eligibility, interventions, endpoints, statistics, and safety/ethics — for expert review. (For non-clinical/UX research, use research-protocol.)
