---
name: followup-sweep
description: Sweep the user's REAL mail and calendar for dropped balls — threads awaiting
  their reply, promises they made, and replies they're owed — then draft the nudges.
  Use when asked what am I forgetting, what have I not replied to, who owes me a reply,
  or chase my open threads in Cowork. Reads sent/received mail via the Gmail connector
  and recent events via Calendar, finds the open loops, and produces a follow-up-list
  artifact plus ready-to-send draft nudges.
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# followup-sweep

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

