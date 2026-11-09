---
name: annual-report-tutor
description: "Use when asked to walk me through an annual report, teach me to read this 10-K, explain a company's accounts to a beginner, or tutor me on the financial statements in an uploaded report. Walks a beginner up a fixed six-rung ladder — statement map, balance sheet line by line, operating profit to free cash flow, five sector-appropriate ratios with healthy ranges, the sceptical read, then a reusable checklist and a five-question quiz. Educational, not financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# annual-report-tutor

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

Produces a page-referenced tutorial in which every figure cites the page it came from and anything missing is marked 'not disclosed in this report'.
