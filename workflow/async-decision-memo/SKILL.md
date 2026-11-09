---
name: async-decision-memo
description: "Run a decision asynchronously — the memo, the silent-read window, the comment protocol, and the deadline that makes it land without a meeting. Use when asked to decide something async, replace a decision meeting with a document, run an Amazon-style written decision process, or when a decision keeps stalling in comment threads. For the document structure alone use decision-memo; this skill runs the process around it."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# async-decision-memo

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

Produces the decision memo plus the process wrapper: reader roles, response windows, comment-resolution rules, and the tie-breaker.
