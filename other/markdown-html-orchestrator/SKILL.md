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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

