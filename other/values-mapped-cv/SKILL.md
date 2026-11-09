---
name: values-mapped-cv
description: "Map a person's achievements to a target company's published values or leadership principles, so the CV leads with the evidence that company says it rewards. Use when asked to align my CV with Amazon's leadership principles, match my experience to this company's values, or which of my achievements fit this company's culture. Uses only the company's public pages, cited with a date."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# values-mapped-cv

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

Produces a value-by-value evidence map with strength ratings, the reordered achievement list for the CV, and the values with no evidence yet.
