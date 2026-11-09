---
name: memory-file-maintenance
description: "Keep your AI memory/context file (MEMORY.md, AGENTS.md, custom instructions) healthy over time — pruning the stale, adding the new, and keeping it sharp so your AI keeps getting you right. Use when asked review my memory file, my AI context is outdated, clean up my AGENTS.md, or maintain my AI instructions."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# memory-file-maintenance

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

Produces a review of your existing memory/instructions file (what's stale, contradictory, bloated, or missing), edits to prune and sharpen it, additions from recent patterns worth remembering, and a light maintenance habit — because a memory file that isn't tended drifts from who you actually are, with a privacy check on what should never be stored.
