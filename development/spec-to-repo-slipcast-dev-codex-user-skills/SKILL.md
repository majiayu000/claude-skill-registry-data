---
name: spec-to-repo
description: 'Use when the user says ''build me an app'', ''create a project from
  this spec'', ''scaffold a new repo'', ''generate a starter'', ''turn this idea into
  code'', ''bootstrap a project'', ''I have requirements and need a codebase'', or
  provides a natural-language project specification and expects a complete, runnable
  repository. Stack-agnostic: Next.js, FastAPI, Rails, Go, Rust, Flutter, and more.'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# spec-to-repo

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

