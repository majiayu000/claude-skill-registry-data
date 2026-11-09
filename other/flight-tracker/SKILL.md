---
name: flight-tracker
description: "Track live aircraft positions with zero API keys — adsb.lol's open ADS-B network primary, OpenSky fallback, via curl: by callsign, registration, or area. Use when asked where is this flight right now, what planes are overhead, track a tail number, or is that flight in the air."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# flight-tracker

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

Produces the live position with altitude, speed, and heading interpreted, the overhead list for a location, and the rerunnable command — with the positions-not-schedules boundary stated honestly.
