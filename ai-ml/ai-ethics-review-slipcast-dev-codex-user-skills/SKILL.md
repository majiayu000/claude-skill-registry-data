---
name: ai-ethics-review
description: "Conduct a structured ethical review of an AI or ML feature, model, or product. Use when preparing to deploy an AI system, assessing algorithmic risk, auditing a model for bias, or producing a responsible AI impact assessment."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-ethics-review

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

Produces a structured ethics review covering fairness, transparency, privacy, safety, accountability, and societal impact with a risk tier score, pre-deployment checklist, and prioritised mitigations.
