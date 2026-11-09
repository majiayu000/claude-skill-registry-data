---
name: world-clock
description: "Get the current time anywhere and convert between time zones with zero API keys — timeapi.io via curl (worldtimeapi fallback), plus the DST-safe meeting-window math. Use when asked what time is it in a city, convert 3pm my time to Tokyo, find a meeting slot across time zones, or what's the UTC offset somewhere."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# world-clock

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

Produces the local time(s), the conversion with DST handled by the API not by memory, and the overlap window for scheduling questions.
