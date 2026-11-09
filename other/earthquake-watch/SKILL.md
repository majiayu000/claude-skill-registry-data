---
name: earthquake-watch
description: "Check recent earthquakes worldwide with zero API keys — USGS real-time GeoJSON feeds via curl, filtered by magnitude, region, and time window. Use when asked was there an earthquake just now, recent quakes near a place, any big earthquakes today, or monitor seismic activity somewhere."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# earthquake-watch

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

Produces the matching events with magnitude, depth, location and time, the felt/damage context bands, and the rerunnable command — with the official-guidance line safety questions require.
