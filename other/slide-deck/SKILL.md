---
name: slide-deck
description: "Build a real, editable PowerPoint (.pptx) deck from an outline or brief. Use when asked to make a slide deck, a PowerPoint, a pitch/board/sales deck as an actual file, or to turn a doc/notes into slides. Requires a code-execution environment (Claude Code, the API code tool, or Claude.ai)."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# slide-deck

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

Produces an actual .pptx via a generated python-pptx script — a title slide, one idea per content slide with a clear headline and concise bullets, and consistent styling.
