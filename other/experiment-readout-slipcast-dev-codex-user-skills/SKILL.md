---
name: experiment-readout
description: "Analyse a finished A/B test and write an honest results readout with real statistics. Use when asked to read out an A/B test, analyse experiment results, check if a result is statistically significant, or decide ship/no-ship from test data. Includes a stdlib significance calculator."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# experiment-readout

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

Produces a readout — the computed lift, p-value & confidence interval, a significance verdict, guardrail check, and a clear ship / no-ship / iterate recommendation.
