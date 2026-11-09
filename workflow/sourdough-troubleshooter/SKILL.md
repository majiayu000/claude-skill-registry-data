---
name: sourdough-troubleshooter
description: "Figure out why the loaf came out dense, flat, or gummy — and what to change next bake. Use when asked why is my sourdough [dense/flat/gummy/not rising], my starter isn't bubbling, help fix my bread, or troubleshoot my sourdough."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# sourdough-troubleshooter

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

Produces a likely-cause diagnosis from your symptoms and process, the specific fix for the next bake, a starter-health check, and a simple timing/temperature adjustment — no dogma, just the variable that's actually off.
