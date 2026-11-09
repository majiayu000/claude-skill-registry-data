---
name: pr-description
description: "Write a clear pull-request description that gets reviewed fast and merged with confidence, from a git diff, branch summary, or commit list. Use when opening a PR, summarizing a change for review, documenting code changes, or asked to write a PR/merge-request description."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# pr-description

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

Produces a structured PR: what changed and why, how it was tested, risk and rollout, and a focused reviewer guide — so the reviewer understands intent before reading a single diff line.
