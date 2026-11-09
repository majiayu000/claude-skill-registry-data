---
name: oncall-handoff
description: "Write a structured end-of-shift on-call handoff so the incoming engineer inherits state, not surprises. Use when asked to write an on-call handoff, oncall handover, shift handoff, pager handoff, or end-of-week SRE summary."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# oncall-handoff

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

Produces a handoff note with open incidents, watchlist alerts, in-flight investigations, recent changes, and one-line asks.
