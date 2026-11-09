---
name: send-approval-check
description: "The gate before an agent sends anything on your behalf: one card showing recipient, sending account, subject, attachments, and the single sentence that commits you to something, so approving the wording is never mistaken for approving the send. Use when asked to check before sending, show me exactly what is about to go out, set up a send approval gate, or review this outgoing email or message an agent drafted."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# send-approval-check

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

Produces the approval card, the commitment sentence quoted, the risk flags, and an explicit approve-the-send question separate from the draft.
