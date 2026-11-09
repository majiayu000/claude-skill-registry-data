---
name: pptx-slide-auditor
description: "Audit a PowerPoint presentation for layout issues, text overflow, visual hierarchy problems, and consistency gaps. Use when asked to review a slide deck, check a presentation before a meeting, audit slides for layout problems, or QA a deck before sharing. Best used with Claude Opus 4.7 or newer for reliable slide-level vision analysis."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# pptx-slide-auditor

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

Produces a slide-by-slide report with issues ranked by severity and specific fixes.
