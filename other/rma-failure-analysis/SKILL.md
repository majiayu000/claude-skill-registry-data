---
name: rma-failure-analysis
description: "Turn field returns into a structured failure-analysis report — RMA triage taxonomy (NTF vs real failures), Pareto by verified failure mode, 8D-style containment→root-cause→corrective-action structure, and cost-of-quality framing. Use when asked to analyse RMA data, investigate field returns, run failure analysis on returned units, write an 8D report, or figure out why return rates are climbing."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# rma-failure-analysis

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

Produces a failure-analysis report with a triage-clean Pareto, 8D actions, and the cost case for fixing each mode.
