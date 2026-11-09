---
name: investment-account-picker
description: "Understand which type of investment/savings account to use for your goal — the tax-advantaged vs taxable question, and which wrapper fits which money. Use when asked which account should I invest in, what's the difference between these account types, where should I put my savings, or tax-advantaged accounts explained. Not financial advice; account types are jurisdiction-specific."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# investment-account-picker

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

Produces a plain-language explainer of the common account categories (retirement/tax-advantaged, general/taxable, education, short-term), a match of your goals to the right account type, the order to prioritize them, and what to verify locally — because using the wrong wrapper can cost you real money.
