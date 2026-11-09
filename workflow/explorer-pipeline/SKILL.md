---
name: explorer-pipeline
description: "Use when asked to make an interactive 3D explorer of a topic from start to finish, go from a topic to a clickable 3D learning page, or run the whole 3D explorer process."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# explorer-pipeline

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

Produces a staged run of explorer-interface-brief, model-prompt-pack and explorer-viewer-builder in order for one topic, with the hand-offs between them, and a build checklist that tracks every asset, source and test until the explorer ships.
