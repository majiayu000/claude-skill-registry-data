---
name: renew-or-churn-call
description: "Score an account's renewal likelihood on a five-level scale with probabilities, and name the next move for the account owner. Use when asked will this account renew, what's the churn risk on this account, should we run a save play, or when a renewal is 30–120 days out and the owner needs a calibrated read rather than a gut feel."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# renew-or-churn-call

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

Produces the account state in a fixed schema, the five-level renewal score with a probability per level and confidence, the mapped next move, and the single signal that would change the call.
