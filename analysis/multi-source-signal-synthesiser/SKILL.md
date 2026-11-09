---
name: multi-source-signal-synthesiser
description: "Synthesises user signals from multiple research sources into a unified, weighted insight brief. Use when you have data from interviews, support tickets, NPS verbatims, app reviews, or sales calls and need to reconcile contradictions, surface the underlying need behind requests, or answer 'what are users really telling us'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# multi-source-signal-synthesiser

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

Produces ranked insights with confidence ratings, source weighting rationale, divergent signal analysis by user segment, and a research gap identification section.
