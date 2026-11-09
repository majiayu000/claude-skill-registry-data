---
name: college-cost
description: "Compute what a degree will actually cost — sticker minus real aid, inflated per year, split into cash and loans, with the loan's decade-long monthly tail made visible before enrollment instead of after. Use when asked what will college really cost, compare these two offers' real prices, how much loan payment after graduation, or is this school affordable."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# college-cost

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

Produces the all-in number from the script, the offer-letter decode (grants vs loans untangled), the monthly-tail reality check, and the two-school comparison.
