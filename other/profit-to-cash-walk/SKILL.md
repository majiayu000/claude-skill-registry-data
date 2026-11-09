---
name: profit-to-cash-walk
description: "Use when asked to reconcile operating profit to free cash flow, walk from EBIT to FCF, explain why profit and cash differ in this report, or show a company's cash conversion from its own accounts. Takes operating profit from an uploaded annual report and walks line by line to free cash flow using the report's own numbers, arithmetic shown at every step. Educational, not financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# profit-to-cash-walk

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

Produces a step table (line, page, amount, running total, one-sentence reason cash and profit diverge), a drift flag on every line where the arithmetic could go wrong, a tie-out to the reported cash flow statement, and an instruction to independently check at least one subtraction.
