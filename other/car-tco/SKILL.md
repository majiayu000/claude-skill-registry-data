---
name: car-tco
description: "Compare the total cost of car ownership across buy-new, buy-used, lease, and keep-your-current-car — depreciation, insurance, maintenance ramp, and fuel over a real horizon, not just the monthly payment. Use when asked should I lease or buy a car, is it cheaper to keep my old car, what does this car really cost per month, or new vs used total cost."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# car-tco

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

Produces the ranked scenario totals, per-month true cost, the assumption ledger, and the not-modeled list.
