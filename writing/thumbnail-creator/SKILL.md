---
name: thumbnail-creator
description: Generate article or newsletter thumbnail candidates using the Gemini
  API from inside Claude Code. Claude reads article copy, proposes composition concepts,
  writes image generation prompts incorporating brand specs, calls Gemini to generate
  the images, evaluates the results via computer vision, and returns ranked candidates
  with rationale. Use when asked to create thumbnails, generate cover images, or produce
  visual candidates for an article or newsletter.
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# thumbnail-creator

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

