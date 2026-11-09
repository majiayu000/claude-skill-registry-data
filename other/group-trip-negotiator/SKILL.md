---
name: group-trip-negotiator
description: "Save the group trip from the group chat — budget alignment before anything gets booked (the awkward conversation, scripted), a decision protocol that actually books things, cost-splitting rules with real numbers for unequal rooms and champagne-taste friends, and the it's-okay-to-split-up daytime clause. Use when someone says 'we're planning a trip with friends and it's chaos', 'how do we split costs', 'one friend wants luxury and one is broke', or the trip has been 'being planned' for three months."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# group-trip-negotiator

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

Produces the budget-alignment script, the decision protocol, and the money agreement.
