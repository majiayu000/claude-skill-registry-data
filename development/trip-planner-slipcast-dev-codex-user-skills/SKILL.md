---
name: trip-planner
description: "Turn a destination, some dates, and your vibe into a realistic day-by-day trip itinerary — paced for real humans, with a packing list and a rough budget. Use when asked to plan a trip, build a travel itinerary, what should I do in [place], or help me plan my holiday."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# trip-planner

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

Produces a day-by-day plan grouped by area (so you're not criss-crossing the city), must-book-ahead flags, a packing list tuned to the trip, a rough budget range, and honest notes on pace and gaps to fill with local info.
