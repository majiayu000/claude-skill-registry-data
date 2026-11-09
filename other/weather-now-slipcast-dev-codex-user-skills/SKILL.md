---
name: weather-now
description: "Get current weather and forecasts with zero API keys — wttr.in one-liners for humans, Open-Meteo JSON for data, with the exact curl commands and format codes. Use when asked what's the weather, will it rain today, forecast for a city, or get me weather data for a location."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# weather-now

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

Produces the live conditions or forecast pulled via curl, interpreted plainly, with the source timestamp and the command used shown so the user can rerun it.
