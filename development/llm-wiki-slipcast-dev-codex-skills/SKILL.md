---
name: llm-wiki
description: Use when building or maintaining a persistent personal knowledge base
  (second brain) in Obsidian where an LLM incrementally ingests sources, updates entity/concept
  pages, maintains cross-references, and keeps a synthesis current. Triggers include
  "second brain", "Obsidian wiki", "personal knowledge management", "ingest this paper/article/book",
  "build a research wiki", "compound knowledge", "Memex", or whenever the user wants
  knowledge to accumulate across sessions instead of being re-derived by RAG on every
  query.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# llm-wiki

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

