---
name: error-message-writer
description: "Write clear, helpful error messages that tell users what happened and how to fix it. Use when asked to write an error message, validation text, a failure/empty-error state, or to rewrite a cryptic system error."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# error-message-writer

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

Produces human, blame-free error copy — what went wrong, why (if useful), and the next step — with options per surface (inline, toast, full page) and the related success/empty states.
