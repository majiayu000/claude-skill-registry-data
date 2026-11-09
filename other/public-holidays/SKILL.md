---
name: public-holidays
description: "Look up public holidays for any country and year with zero API keys — the Nager.Date API via curl, with long-weekend detection and cross-country planning. Use when asked what are the holidays in a country, is date X a holiday somewhere, find long weekends this year, or which days is the team in Japan and Germany both off."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# public-holidays

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

Produces the holiday list with local names, the specific-date answer, long-weekend candidates, and the rerunnable command.
