---
name: metric-tree-builder
description: "Decompose a north-star metric into a driver tree — the inputs and sub-inputs that actually move it — so a team knows which levers to pull. Use when asked to build a metric tree, break down a north-star metric, map metric drivers, or find the inputs behind an output metric."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# metric-tree-builder

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

Produces a hierarchical tree from the top metric down to actionable input metrics, with the relationships, the highest-leverage levers, and what to instrument.
