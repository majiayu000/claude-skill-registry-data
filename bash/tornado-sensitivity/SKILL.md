---
name: tornado-sensitivity
description: "Which assumption actually moves the answer — one-at-a-time sensitivity, ranked into a tornado. Use when a model's output is being argued about (LTV, ROI, forecast) and the room is debating drivers that don't matter, or before spending diligence effort: swing every driver low→high and see which one owns the outcome."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# tornado-sensitivity

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

Produces the ranked tornado table, share-of-swing per driver, and a real .xlsx — via the bundled zero-dependency script with a safely restricted formula evaluator.
