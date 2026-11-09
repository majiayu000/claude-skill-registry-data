---
name: notebooklm
description: Browser automation skill for controlling Google's NotebookLM. Use when
  the user wants anything done in NotebookLM (e.g., 'open NotebookLM', 'check my [name]
  notebook', 'ask my notebook about X', 'add [source] to NotebookLM', 'generate a
  Video Overview from my notebook', 'use NotebookLM Studio'). Handles reading and
  querying notebooks, adding sources (URLs, text, files, YouTube links, synthesized
  content), generating Studio outputs (Audio/Video Overviews, Mind Maps, Reports incl.
  Briefing Doc/Study Guide/FAQ, Flashcards, Quiz, slide decks, infographics — discover
  the exact set from the live Studio panel; the UI evolves fast), and creating new
  notebooks. Requires browser automation environment — fails gracefully when unavailable.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# notebooklm

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

