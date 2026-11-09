---
name: company-compare-same-definitions
description: "Use when asked to compare two annual reports, put two companies from the same sector side by side, or check whether two companies' adjusted numbers mean the same thing. Takes two uploaded annual reports from one sector and compares them on five ratios computed with identical definitions from audited figures, flagging every place the companies define a metric differently. Educational, not financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# company-compare-same-definitions

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

Produces a page-referenced comparison table, a definitions-differ section (adjusted vs statutory, inside vs outside the audited statements), and three questions to ask before believing either company's highlights.
