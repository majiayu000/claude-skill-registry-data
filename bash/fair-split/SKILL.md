---
name: fair-split
description: "Divide things that cannot be divided — an inherited house, a dissolved partnership, the furniture after a breakup — using sealed-bid fair division (Knaster), computed by the bundled script so everyone ends provably above their own fair share. Use when asked to split an estate fairly, divide assets between siblings or ex-partners, who gets the house and what do they owe the others, or handle unequal shares. Math for the family meeting; not legal advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# fair-split

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

Produces the sealed-bid procedure, the computed allocation with exact cash transfers, the per-person fairness proof, and the presentation script.
