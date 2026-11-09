---
name: replica-test
description: 'Clicks through every flow of an app clone and tests it for bugs: a test
  plan generated from the recon flows with happy paths and edge cases, Playwright
  end-to-end tests where possible, a browser click-through where not, and bug reports
  in a fixed format with severity, steps and evidence. Use when the user says "test
  my clone", "find bugs", "QA this", "click through everything", "write e2e tests",
  "does it work", or after /replica-build or /replica-backend.'
metadata:
  source-package: replica-skill-main
  adapted-for: Codex
---

# replica-test

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

