---
name: inventory-policy
description: "Set inventory policy for an item class: segmentation, safety stock, and replenishment method. Use when asked to set safety stock levels, segment items by ABC/XYZ, choose reorder points vs min-max, define stocking policy, or review excess and obsolete inventory."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# inventory-policy

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

Produces a segmentation grid, per-segment service targets and safety-stock logic, a replenishment method choice per segment, and an E&O review cadence.
