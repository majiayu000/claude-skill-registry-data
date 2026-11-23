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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

