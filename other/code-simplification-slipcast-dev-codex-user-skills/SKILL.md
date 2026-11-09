---
name: code-simplification
description: "Simplify code that works — remove speculative abstraction, dead flexibility, and needless indirection while keeping behaviour identical and verified. Use when a feature has just landed ('now simplify it'), when AI-generated code arrives over-engineered, when a file has grown hard to follow, or as the cleanup pass before review. For finding bugs use code-review-checklist / ai-code-review — this skill assumes it works and makes it simple."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# code-simplification

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

Produces a smaller, flatter version with identical behaviour, plus a ledger of what was removed and why it was safe.
