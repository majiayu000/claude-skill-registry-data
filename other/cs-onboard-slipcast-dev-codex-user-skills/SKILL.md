---
name: cs-onboard
description: Founder onboarding interview that captures company context across 7 dimensions.
  Invoke with /cs-onboard setup for initial interview or /cs-onboard update for quarterly
  refresh. Generates ~/.claude/company-context.md used by all C-suite advisor skills.
  Use when setting up the C-suite advisors for the first time, or when company context
  is missing or more than 90 days old — e.g. after a fundraise or pivot.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# cs-onboard

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
