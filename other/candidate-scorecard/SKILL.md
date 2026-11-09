---
name: candidate-scorecard
description: "Turn interview notes into a structured candidate scorecard and hire recommendation. Use when asked to write an interview scorecard, a candidate evaluation, an interview debrief, or to summarize feedback into a hire/no-hire call."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# candidate-scorecard

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

Produces a per-competency assessment with evidence and ratings, an overall recommendation with confidence, and the open questions for the next round — evidence-based, bias-aware, and decision-ready.
