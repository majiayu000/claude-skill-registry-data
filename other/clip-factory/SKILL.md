---
name: clip-factory
description: "Turn one long video, podcast, or stream transcript into 8-12 short-form clips — each with a hook line, cut timestamps, captions, and a platform note for TikTok/Reels/Shorts — plus an honesty gate that kills clips that misrepresent the source. Use when someone says 'clip this podcast', 'make shorts from my video', 'what's clippable here', or runs a clipping side hustle."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# clip-factory

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

Produces a ranked clip sheet ready for an editor or a clipping app.
