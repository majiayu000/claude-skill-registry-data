---
name: brainstorming
description: "Run a real brainstorm — divergent generation without judgment, then convergent selection with explicit criteria — instead of listing ten obvious ideas and calling it creativity. Use when asked to brainstorm, generate ideas or options, explore a solution space, or name something."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# brainstorming

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

Produces a genuinely wide option set (including the weird tail), then a shortlist selected against named criteria with the rejects preserved.
