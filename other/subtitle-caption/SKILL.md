---
name: subtitle-caption
description: "Write or translate subtitles/captions that respect reading speed and timing rules. Use when asked to write subtitles, captions, SRT/VTT content, or to translate subtitles for a video."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# subtitle-caption

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

Produces properly-formatted, readable subtitles — line-length and reading-speed compliant, well-segmented, with translation that fits the time available, plus SDH/caption guidance where relevant.
