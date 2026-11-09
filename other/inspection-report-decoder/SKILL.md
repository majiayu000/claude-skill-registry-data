---
name: inspection-report-decoder
description: "Decode a home inspection report into what's cosmetic, what's expensive, and what kills deals — with repair-cost ranges and the negotiation list. Use when asked to decode my inspection report, is this inspection bad, what should I ask the seller to fix, or should I walk after inspection."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# inspection-report-decoder

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

Produces a findings triage (walk-risk / negotiate / cosmetic), cost ranges per item, the ask-the-seller list, and the questions for your inspector before the objection deadline.
