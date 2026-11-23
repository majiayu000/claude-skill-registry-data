---
name: markdown-html-orchestrator
description: Use when a user wants to convert any markdown file in their Claude project
  into a single-file, lightly-interactive HTML — long-form documents (specs, plans,
  RFCs, reports, explainers), code reviews with diffs and severity-tagged annotations,
  or slide decks. Triggers on "convert this markdown to HTML", "make this an HTML
  file", "turn this into an interactive document", "render this report as HTML", "PR
  writeup as HTML", "slides from this markdown". Forks context to route to one of
  three converter sub-skills (md-document, md-review, md-slides) based on a deterministic
  doctype classifier, after the user has run the design-system onboarding once. Refuses
  if input is under 100 lines (per Shihipar — markdown still wins below the threshold)
  or design-system isn't onboarded.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# markdown-html-orchestrator

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

