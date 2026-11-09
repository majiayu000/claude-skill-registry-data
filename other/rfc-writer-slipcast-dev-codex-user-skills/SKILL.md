---
name: rfc-writer
description: "Write an engineering RFC (Request for Comments) for a technical decision, architectural change, or significant implementation approach. Use when asked to write an RFC, document a technical proposal, create a design doc, write an architecture decision for review, or produce a technical specification for team feedback."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# rfc-writer

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

Produces a complete RFC document covering problem statement, motivation, proposed solution, alternatives rejected, implementation plan, migration plan, security and performance implications, observability changes, rollout plan, and open questions.
