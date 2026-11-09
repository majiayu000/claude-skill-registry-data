---
name: focused-fix
description: 'Use when the user asks to fix, debug, or make a specific feature/module/area
  work end-to-end. Triggers: ''make X work'', ''fix the Y feature'', ''the Z module
  is broken'', ''focus on [area]''. Not for quick single-bug fixes — this is for systematic
  deep-dive repair across all files and dependencies.'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# focused-fix

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

