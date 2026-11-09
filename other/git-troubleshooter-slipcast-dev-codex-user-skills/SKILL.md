---
name: git-troubleshooter
description: "Diagnose a tangled git situation and give the exact, safe commands to fix it. Use when asked to undo a commit, recover lost work, fix a bad merge or rebase, resolve a detached HEAD, unstage files, or get out of a git mess."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# git-troubleshooter

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

Produces the diagnosis, the precise commands to run in order, what each does, and a recovery note if something goes wrong.
