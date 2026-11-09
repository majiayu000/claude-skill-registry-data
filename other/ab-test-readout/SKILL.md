---
name: ab-test-readout
description: "Analyse a finished A/B test and write the readout — the result, whether it's statistically and practically significant, what it means, and the ship/no-ship call. Use when asked to analyse experiment results, write an A/B test readout, interpret test data, or decide whether to ship a variant. Distinct from planning a test — this reads results."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ab-test-readout

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

Produces a clear verdict with the lift and confidence, segment cuts, the risks (peeking, novelty, sample), and a recommendation.
