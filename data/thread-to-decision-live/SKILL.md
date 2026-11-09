---
name: thread-to-decision-live
description: Turn a REAL Slack thread (or channel) into a logged decision — read it,
  extract what was decided, who owns what, and record it in Notion — not a template
  for writing decisions. Use when asked to capture the decision from this thread,
  log what we agreed, turn this Slack discussion into a decision record, or close
  this out in Cowork. Reads the thread via the Slack connector, distils the decision
  / owners / next steps / open questions, and produces a decision-record artifact
  written to a Notion database (with the source thread linked).
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# thread-to-decision-live

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

