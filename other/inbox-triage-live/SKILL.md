---
name: inbox-triage-live
description: "Triage the user's REAL inbox through the Gmail connector — not a framework they run by hand. Use when asked to clear my inbox, get me to inbox zero on the actual account, triage my unread, or process my email backlog in Cowork. Reads unread via the Gmail connector, sorts every message into archive / reply-now / task / park, applies labels and archives in place, drafts the reply-now messages as real Gmail drafts."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# inbox-triage-live

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

Produces a triage-report artifact of what it did and what still needs the user.
