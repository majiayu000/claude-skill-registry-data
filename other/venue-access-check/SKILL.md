---
name: venue-access-check
description: "Check whether a specific venue — a restaurant, office, event space, Airbnb, clinic — will actually work for your access needs, before you commit, with the exact questions to ask and the red flags in the answers. Use when someone says 'will this place work for my wheelchair', 'check if this venue is accessible', 'questions to ask a venue about access', or 'is this restaurant/office actually accessible'. For personal access decisions; not a formal accessibility audit."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# venue-access-check

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

Produces a tailored question list, how to read the answers, and a go/adapt/avoid verdict.
