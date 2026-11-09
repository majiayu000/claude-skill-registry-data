---
name: interview-me
description: "Elicit the real requirements by interviewing the requester BEFORE building or writing anything — one question at a time, until the brief is buildable. Use when a request is vague ('make me a dashboard', 'write something for the board'), when past deliverables missed the mark, or when the user says 'interview me' / 'ask me questions first'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# interview-me

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

Produces a validated brief: goal, audience, constraints, success criteria, and explicit non-goals — then, and only then, the work.
