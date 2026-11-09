---
name: notebooklm-connector
description: "Automates NotebookLM from Claude Code using browser automation via the Claude Chrome extension — creating notebooks, adding sources, and triggering outputs without manual clicking. Use when you want to create a NotebookLM notebook, add URLs or documents as sources, or generate mindmaps, audio overviews, or briefing docs programmatically."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# notebooklm-connector

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

Produces a confirmed checklist of completed actions and a direct link to the notebook.
