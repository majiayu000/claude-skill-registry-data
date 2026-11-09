---
name: context-mode
description: "Keep Claude Code sessions productive across resets with output filtering, session logging, and auto-resume. Use when starting a long or complex coding session, when previous sessions lost context mid-task, or when you need Claude to resume exactly where it left off after a reset."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# context-mode

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

Produces a session.log at the project root, filtered command output that preserves context, and automatic resume of in-progress tasks after any reset.
