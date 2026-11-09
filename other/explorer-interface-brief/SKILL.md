---
name: explorer-interface-brief
description: "Use when asked to design the interface for an interactive 3D explorer, plan a UI for exploring a 3D model of a topic, or write an image-model prompt for a 3D learning app mock-up. First step of explorer-pipeline."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# explorer-interface-brief

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

Produces, from a topic, the UI design brief (audience, layout, panels, interactions, label style, colour palette, accessibility) and an image-model prompt for the interface mock.
