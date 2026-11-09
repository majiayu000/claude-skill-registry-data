---
name: context-engineering-review
description: "Review what an LLM feature or agent actually puts in its context window — and find what's bloating, missing, or fighting itself. Use when asked to review a system prompt and context assembly, cut token usage without losing quality, debug an agent that ignores instructions, or audit how retrieval results, history, and tool definitions are packed into the window. For wording-level prompt tuning use prompt-optimizer."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# context-engineering-review

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

Produces a context inventory with a keep/cut/restructure verdict per component, ordering and caching fixes, and a token budget.
