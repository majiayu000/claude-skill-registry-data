---
name: formula-detangler
description: "Untangle the spreadsheet formula nobody dares touch — decompose the seven-function nest into named readable steps, explain what it actually does (vs. what it's believed to do), and rebuild it maintainably with helper columns and modern functions. Use when asked what does this formula do, this IFERROR-VLOOKUP monster broke, make this formula maintainable, or nobody understands the sheet the analyst left."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# formula-detangler

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

Produces the plain-language decode, the step decomposition into helper columns, the believed-vs-actual gaps, and the rebuilt version.
