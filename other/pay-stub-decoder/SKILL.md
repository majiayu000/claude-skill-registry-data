---
name: pay-stub-decoder
description: "Decode a pay stub line by line — every deduction explained, the gross-to-net story, and the errors worth catching. Use when asked to explain my pay stub, why is my paycheck smaller than expected, what are all these deductions, or check my paycheck for mistakes."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# pay-stub-decoder

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

Produces a line-by-line decode, the gross-to-net waterfall, the error checklist (withholding, benefits, overtime), and the fixes to raise with payroll.
