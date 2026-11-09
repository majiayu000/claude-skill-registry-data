---
name: feature-prioritisation
description: "Apply prioritisation frameworks (RICE, MoSCoW, Kano, ICE, Opportunity Scoring) to rank features and backlog items. Use when asked to prioritise features, rank a backlog, decide what to build next, or evaluate tradeoffs between competing ideas."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# feature-prioritisation

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

Produces a scored, ranked feature list with framework-specific tables, recommended build order, deprioritised items, and assumptions made.
