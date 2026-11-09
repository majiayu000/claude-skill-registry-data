---
name: empty-state-writer
description: "Write empty-state content that turns a blank screen into a next step. Use when asked to write an empty state, a zero-data / first-run state, a no-results state, or onboarding placeholder content."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# empty-state-writer

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

Produces empty-state copy — a clear headline, a helpful line, and a primary action — for each type (first-use, user-cleared, no-results, error/permission), so a blank screen guides instead of confuses.
