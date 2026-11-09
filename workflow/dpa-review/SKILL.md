---
name: dpa-review
description: "Read a Data Processing Agreement before you sign it — sub-processors, transfer mechanism, breach-notice window, deletion, audit rights — in plain language with 🔴🟡🟢 risk. Use when asked to review a DPA, check a data processing agreement, is this DPA safe to sign, or what am I agreeing to on data."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# dpa-review

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

Produces the plain-English summary, the risk-ranked findings, the missing-clause checklist, and the questions to send back before signature.
