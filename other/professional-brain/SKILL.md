---
name: professional-brain
description: "Maintain a durable, local markdown memory ('brain') of your product context, decisions, hypotheses, and stakeholders that other skills read from and write back to. Use when asked to set up a brain, ingest notes/artifacts into memory, recall what's known about a topic, log a decision with provenance, or run a weekly brain review."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# professional-brain

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

Produces a structured brain/ folder (knowledge, decisions, hypotheses, stakeholders, entities, source) with provenance-tagged facts, plus ingest/recall/record/review operations with approval-gated, append-only write-back.
