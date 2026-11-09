---
name: payroll-eve-check
description: "Have a proactive agent check payroll the day before it runs in Gusto, Deel, Xero Payroll or similar: unusual pay changes, new starters and leavers, missing approvals, enough cash in the funding account, and anything that would make a payslip wrong, reported as a short pre-run list for a human to approve. Use when asked to check payroll before it runs, catch payroll mistakes, have Duet review Gusto before payday, pre-payroll checklist, or alert me if payroll looks wrong."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# payroll-eve-check

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

Produces the pre-run checks, the anomaly list with each line's evidence, the funding check, and the questions for the payroll owner; it never runs, edits or approves payroll.
