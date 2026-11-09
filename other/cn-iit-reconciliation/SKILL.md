---
name: cn-iit-reconciliation
description: "Prepare for China's annual individual income tax reconciliation (个税年度汇算): check income, deductions and special additional deductions, compare the two treatments of a year-end bonus, and estimate the refund or amount to pay before filing in the 个人所得税 app. Use when asked 个税汇算怎么弄, 年终奖单独计税还是合并, 我能退多少税, 专项附加扣除, or how does China's annual tax reconciliation work. Not tax advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-iit-reconciliation

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

Produces a filing checklist, the deductions the person may be missing, a bonus comparison, the estimate with workings, and deadlines.
