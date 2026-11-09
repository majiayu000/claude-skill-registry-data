---
name: rss-digest
description: "Fetch and digest any RSS or Atom feed with zero API keys — curl plus disciplined parsing into a ranked, deduplicated briefing instead of a link dump. Use when asked summarize this feed, what's new on this blog, digest these RSS feeds, or build me a morning briefing from these sources."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# rss-digest

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

Produces the digest with dates and one-line what-it-is summaries, cross-feed dedup, and the rerunnable commands per feed.
