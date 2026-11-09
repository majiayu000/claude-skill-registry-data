---
name: inbox-zero-operator
description: "Drive an email inbox to zero through a computer-use or tool-using agent — triage every message into act/delegate/defer/archive with drafts prepared, never a send. Use when asked to get my inbox to zero, triage my email hands-on, process my inbox for me, or run inbox zero."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# inbox-zero-operator

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

Produces the triage ledger, prepared reply drafts, and an approval-gated action plan the agent then executes read-mostly.
