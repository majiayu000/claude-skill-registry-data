---
name: code-review-guide
description: "Review a pull request or diff like a thoughtful senior engineer — prioritized, kind, and focused on what matters. Use when reviewing code, giving PR feedback, or asked to 'review this change'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# code-review-guide

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

Produces a structured review: a correctness/design pass, comments ranked by severity (blocking → nit), what's done well, and a clear approve / request-changes call — feedback that improves the code and the author.
