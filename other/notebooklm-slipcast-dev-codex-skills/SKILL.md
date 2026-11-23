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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

