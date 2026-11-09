---
name: md-slides
description: Converts a markdown deck (slides separated by `---` HR boundaries or
  by `# ` H1 headings, with optional HTML-comment `notes:` presenter-notes blocks)
  into a single-file HTML presentation with arrow-key / space / PgDn / PgUp / Home
  / End / P / Esc keyboard navigation, presenter mode (split view with current slide
  + speaker notes + clock + next-slide preview), URL-hash deep linking, and `@media
  print` page-per-slide for PDF export. Triggers when the markdown-html-orchestrator
  classifies an input as SLIDES, or when invoked directly via /cs-md-slides. Reuses
  md-document's markdown parser for slide-body rendering and reads design-system tokens
  via config_loader.py. Refuses if input has no clear slide boundaries, produces a
  1-slide deck, or `--strict-notes` is on with under 50% notes coverage. Use after
  orchestrator routing.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# md-slides

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

