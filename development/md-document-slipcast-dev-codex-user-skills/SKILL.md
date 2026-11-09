---
name: md-document
description: Converts long-form markdown (specs, RFCs, reports, plans, explainers)
  into a single-file, lightly-interactive HTML document with sticky TOC, scrollspy,
  search filter, code-copy buttons, and design-system-driven brand tokens. Triggers
  when the markdown-html-orchestrator classifies an input as DOCUMENT, or when invoked
  directly via /cs-md-document. Reads the design-system config via config_loader.py
  and inlines the user's 12 derived CSS custom properties; refuses to render if onboarding
  hasn't run. Single-file output — Google Fonts + Prism.js CDN are the only externals;
  no framework runtime, no build step. Use after orchestrator routing or after design-system
  onboarding is confirmed.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# md-document

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

