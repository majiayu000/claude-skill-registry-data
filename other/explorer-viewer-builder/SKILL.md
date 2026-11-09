---
name: explorer-viewer-builder
description: "Use when asked to build a 3D viewer for a GLB model, make an interactive explorer with clickable labelled parts, add an exploded view or quiz to a 3D model, or turn a parts list into a web page. Third step of explorer-pipeline."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# explorer-viewer-builder

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

Produces a single-file Three.js viewer that loads GLB models, with orbit controls, clickable labelled parts, an exploded view toggle and a quiz mode, built from the tested template in references/viewer-template.html.
