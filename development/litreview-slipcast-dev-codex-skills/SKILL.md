---
name: litreview
description: Searches academic literature through free, keyless PubMed and OpenAlex
  APIs, optionally augments results with Consensus MCP when connected, builds a PICO,
  SPIDER, decomposition, or hybrid search plan, and produces a formatted Word research-orientation
  guide. Uses brief intake and post-reconnaissance checkpoints to confirm the framework,
  sub-areas, and depth (5, 10, or 20 queries) before spending the search budget. The
  output is a launching pad, not a finished review. Use when the user requests a literature
  review, starts a paper or literature-oriented research project, or needs structured
  research on a topic. Do NOT use for a single paper lookup or a quick paper list;
  use a plain PubMed, OpenAlex, or Consensus query instead.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# litreview

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

