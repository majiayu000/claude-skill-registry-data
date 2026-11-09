---
name: notes-humanizer
description: "Strips AI writing patterns from text and rewrites it to sound genuinely human — removing the statistical defaults, then adding earned voice calibrated to genre (opinion pieces get a person's voice; docs and summaries stay neutral) without ever faking humanity. Use when a draft reads as AI-generated, over-polished, or rhythmically uniform — including blog posts, emails, LinkedIn posts, or any prose that needs to sound like a real person wrote it."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# notes-humanizer

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

Produces a pattern audit, side-by-side comparison, itemised change log, and clean rewritten output ready to paste.
