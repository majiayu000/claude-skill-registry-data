---
name: sun-and-moon
description: "Get sunrise, sunset, golden hour, day length, and moon phase for any location with zero API keys — sunrise-sunset.org and Open-Meteo via curl, times converted to local. Use when asked when is sunset today, golden hour for a photo shoot, how long is the day, what's the moon phase tonight, or sun times for a date and place."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# sun-and-moon

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

Produces the sun/moon times in the user's local zone (the UTC trap handled), the photography windows, and the rerunnable command.
