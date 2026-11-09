---
name: code-tour
description: 'Use when the user asks to create a CodeTour .tour file — persona-targeted,
  step-by-step walkthroughs that link to real files and line numbers. Trigger for:
  create a tour, onboarding tour, architecture tour, PR review tour, explain how X
  works, vibe check, RCA tour, contributor guide, or any structured code walkthrough
  request.'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# code-tour

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

