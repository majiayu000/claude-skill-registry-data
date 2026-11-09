---
name: model-prompt-pack
description: "Use when asked to write prompts for image-to-3D or text-to-3D tools, generate 3D models of a topic's parts, plan the assets for a 3D explorer, or build a labelled parts list with sources. Second step of explorer-pipeline."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# model-prompt-pack

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

Produces prompts for image-to-3D tools, one per object, plus a parts list for labelling in which every label names a trusted source, and states that generated geometry is illustrative, not authoritative.
