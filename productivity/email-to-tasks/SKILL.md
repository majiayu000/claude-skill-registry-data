---
name: email-to-tasks
description: "Convert an email (or a whole thread) into real tasks — the actual asks extracted from the prose, each with owner, deadline, and the done-test, so nothing lives in the inbox as its own reminder. Use when asked what am I actually being asked to do here, turn this thread into a task list, extract the action items from this email, or I keep re-reading this thread."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# email-to-tasks

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

Produces the ask extraction with quoted sources, the task list in owner-verb-deadline form, and the reply that confirms the commitments.
