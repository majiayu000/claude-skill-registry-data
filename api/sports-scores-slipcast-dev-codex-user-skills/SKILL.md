---
name: sports-scores
description: "Get live scores, schedules, and standings for major leagues with zero API keys — ESPN's public JSON endpoints via curl, covering NFL, NBA, MLB, NHL, and world football. Use when asked what's the score, did my team win, today's games, or league standings right now."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# sports-scores

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

Produces the scores with game state (live/final/scheduled), the asked-team answer first, and the rerunnable command — with the unofficial-API caveat stated.
