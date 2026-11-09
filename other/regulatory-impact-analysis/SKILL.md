---
name: regulatory-impact-analysis
description: "Produce a regulatory impact analysis (RIA) weighing the costs, benefits, and alternatives of a proposed rule. Use when asked to assess a regulation's impact, do a cost-benefit analysis of a policy, justify a rulemaking, or compare regulatory options."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# regulatory-impact-analysis

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

Produces a structured RIA: the problem and rationale, options including the baseline, costs vs. benefits, distributional effects, and a reasoned recommendation.
