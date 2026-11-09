---
name: board-game-night-planner
description: "Plan a board game night that actually lands — the right games for your group size, mix, and time, in a running order that keeps energy up. Use when asked to plan a game night, what board game should we play, games for [N] people, or what to play with a mixed group."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# board-game-night-planner

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

Produces game picks matched to player count and experience, a warm-up-to-main running order, teach-time and play-time estimates, and swaps for the non-gamers or the one player who hates losing.
