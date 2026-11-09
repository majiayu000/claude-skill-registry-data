---
name: replica-build
description: 'Rebuilds an app screen by screen from the recon map: app shell first,
  then the core flow as a vertical slice, then every screen with all its states, ticking
  off the feature matrix as it goes. Writes every line fresh, never the original''s
  code, assets or copy. Use when the user says "build the clone", "build screen S07",
  "start building", "rebuild this screen", "implement the booking page", or after
  /replica-design.'
metadata:
  source-package: replica-skill-main
  adapted-for: Codex
---

# replica-build

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

