---
name: karaoke-song-picker
description: "Pick the karaoke song that actually fits your voice and the room — so you land it instead of dying on a key change. Use when asked what karaoke song should I sing, pick me a karaoke song, what should I sing for [occasion], or a song for my voice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# karaoke-song-picker

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

Produces a few tailored song picks matched to your range and skill, why each works (and the tricky bit to watch), a crowd-pleaser vs a show-off pick, a group/duet option, and a safe fallback for when nerves hit.
