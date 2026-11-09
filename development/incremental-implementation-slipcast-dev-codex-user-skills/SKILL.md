---
name: incremental-implementation
description: "Build in small, individually-verified increments that each leave the system working — instead of big-bang changes that fail mysteriously at the end. Use when implementing multi-part features, refactoring anything load-bearing, making large mechanical changes, or when past work produced huge diffs that were wrong somewhere unfindable."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# incremental-implementation

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

Produces the same end state as the big bang, reached through verified checkpoints you can stop at, ship from, or roll back to.
