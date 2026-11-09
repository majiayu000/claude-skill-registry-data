---
name: hn-digest
description: "Pull the current Hacker News front page, top comments, or a topic search with zero API keys — the official Firebase API and Algolia search via curl, digested instead of dumped. Use when asked what's on Hacker News, summarize HN today, what's the discussion on this story, or has HN covered some topic."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# hn-digest

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

Produces a ranked digest with scores and comment counts, the discussion's actual argument threads when asked, and the rerunnable commands.
