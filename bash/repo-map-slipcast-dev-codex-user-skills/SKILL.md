---
name: repo-map
description: "Navigate a codebase by map instead of reading files wholesale — a deterministic stdlib script that emits the tree with line counts and top-level symbols, plus the read-the-map-first discipline that cuts exploration tokens by an order of magnitude. Use when asked explore this repo efficiently, stop re-reading the whole codebase, make a map of this project, or which files should the agent actually open."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# repo-map

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

Produces the compact map with its token math (map vs. everything), the navigation discipline, and the open-only-what-matches rule.
