---
name: figma-design-qa
description: "Runs a pre-handoff QA checklist on a Figma design before it goes to engineering. Use when asked to QA a Figma design, do a pre-handoff check, or validate a Figma file is ready to build. Optimised for Opus 4.7 and newer models."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# figma-design-qa

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

Produces a structured QA report covering file hygiene, component usage, accessibility, and handoff readiness with explicit pass/fail status per item.
