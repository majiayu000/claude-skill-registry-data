---
name: air-quality
description: "Check live air quality anywhere with zero API keys — Open-Meteo's air-quality API via curl, decoded from raw PM2.5 and AQI numbers into what they mean for going outside. Use when asked what's the air quality, is it safe to run outside, AQI in my city, or pollution levels right now."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# air-quality

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

Produces the current AQI and pollutant levels, the plain-language health read with the standard bands, and the rerunnable command.
