---
name: home-inspection-decoder
description: "Make sense of a home-inspection report before you buy — what's serious vs cosmetic, what to negotiate, and what to investigate further. Use when asked to explain my home inspection, is this inspection finding serious, what should I negotiate after inspection, or decode my inspection report."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# home-inspection-decoder

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

Produces a triage of findings by severity (safety/structural/expensive vs minor/cosmetic), plain-English translations, the items worth a repair credit or price negotiation, what warrants a specialist follow-up, and a walk-vs-proceed read — flagging that the inspector and specialists are the authority.
