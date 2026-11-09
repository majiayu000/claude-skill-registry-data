---
name: runway-monte-carlo
description: "Cash runway as a distribution, not a number — Monte Carlo simulated. Use when someone asks how long their cash lasts, when to start fundraising, or how burn/revenue volatility changes their runway; especially when the naive cash÷burn answer is driving a decision."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# runway-monte-carlo

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

Produces P10/P50/P90 runway, month-by-month death probabilities, and a real .xlsx with editable assumptions and a live naive-runway formula — via the bundled zero-dependency simulator.
