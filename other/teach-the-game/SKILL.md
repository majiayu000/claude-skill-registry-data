---
name: teach-the-game
description: "Build a 5-minute teach script for any board game so the table starts playing instead of listening — theme first, goal second, a turn third, exceptions only when they come up. Use when someone says 'how do I explain Catan/Wingspan/this game', 'teaching my family a game tonight', 'my rules explanations kill the mood', or 'make a teach script'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# teach-the-game

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

Produces a spoken-word teach script with a first-turn walkthrough and a what-to-skip list.
