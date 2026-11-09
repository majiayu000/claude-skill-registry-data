---
name: birdwatching-log
description: "Get started birding from where you are — what you're likely to see, how to tell confusing species apart, and a simple life-list to track sightings. Use when asked to start birdwatching, what bird did I see, help me identify a bird, or set up a birding log."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# birdwatching-log

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

Produces a likely-species list for your area and season, ID prompts (the field marks and sounds that separate look-alikes), a beginner gear-and-timing note, and a lightweight life-list format — pointing you to a live ID app to confirm any specific sighting.
