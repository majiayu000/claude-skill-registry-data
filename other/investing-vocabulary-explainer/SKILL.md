---
name: investing-vocabulary-explainer
description: "Use when asked what a term means in an annual report, to explain EBITDA, goodwill, free cash flow, working capital or diluted EPS, or to define any investing or accounting word in plain English, ideally in the context of an uploaded report. Explains each term the user gives, anchored to the specific document where one is provided. Refuses buy, sell and valuation opinions and points to the other skills in the bundle instead. Educational, not financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# investing-vocabulary-explainer

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

Produces, per term, a one-sentence plain definition, where it appears in this document with the page, why a beginner might misread it, and one thing to check next.
