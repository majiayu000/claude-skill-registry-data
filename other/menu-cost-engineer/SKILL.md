---
name: menu-cost-engineer
description: "Cost a menu item to a plate cost and food-cost percentage, then price it for a target margin. Use when asked to cost a dish, calculate food cost percentage, price a menu item, or engineer a menu for profitability."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# menu-cost-engineer

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

Produces a plate-cost breakdown (ingredient × yield × price), the food-cost %, a suggested price for the target margin, and menu-engineering flags (star / plow-horse / puzzle / dog) so the operator knows what to promote, reprice, or cut.
