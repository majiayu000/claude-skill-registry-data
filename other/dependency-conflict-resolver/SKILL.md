---
name: dependency-conflict-resolver
description: "Resolve a dependency or version conflict (npm, pip, yarn, pnpm, Maven, Go modules) step by step. Use when an install fails with peer-dependency or version-conflict errors, packages won't co-exist, or a lockfile is fighting you."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# dependency-conflict-resolver

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

Produces the conflict explained, the resolution options ranked by safety, exact commands, and how to keep it from recurring.
