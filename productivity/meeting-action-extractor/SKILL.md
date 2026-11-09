---
name: meeting-action-extractor
description: "Pull the action items and decisions out of meeting notes or a transcript — each with an owner, a due date, and enough context to become a ticket — plus the open questions. Use when asked to extract action items, turn these notes into tasks, who owns what from this meeting, or pull the to-dos from this transcript."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# meeting-action-extractor

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

Produces the ticket-ready action list (owner + due + context), the decisions made, the open questions with no owner yet, and a flag for any 'someone should…' that never got assigned.
