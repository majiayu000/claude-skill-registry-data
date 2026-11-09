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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

