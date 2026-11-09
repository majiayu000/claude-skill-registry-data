---
name: game-night-planner
description: "Plan a game night that actually works for the specific people coming — the right lineup for player count, weight tolerance, and time, sequenced from icebreaker to main event, with the fallback for when someone bails. Use when someone says planning a game night, what board game should we play, games for six people, my partner hates long games, or we always end up arguing over what to play."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# game-night-planner

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

Produces a sequenced lineup with reasoning, teach-time and play-time estimates, swaps for the non-gamers, and a plan B.
