---
name: git-worktree-manager
description: Run parallel feature work safely with Git worktrees. Standardizes branch
  isolation, port allocation, environment sync, and cleanup so each worktree behaves
  like an independent local app. Optimized for multi-agent workflows where each agent
  or terminal session owns one worktree. Use when running multiple feature branches
  simultaneously, isolating experimental work, or coordinating multi-agent development
  across the same repo.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# git-worktree-manager

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

