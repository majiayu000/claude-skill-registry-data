---
name: synthetic-user-research
description: "Use AI personas for early-stage research signal — with hard guardrails on what synthetic methods can and cannot validate. Use when asked to run synthetic user testing, simulate user reactions with AI personas, pretest a survey or message before fielding it, or decide whether synthetic research is appropriate at all. Never a substitute for discovery interviews — see discovery-interview-guide and user-research-synthesis for the real thing."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# synthetic-user-research

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

Produces a fit verdict for the question at hand, a persona-panel design grounded in real data, the findings labelled as synthetic throughout, and the follow-up plan with real humans.
