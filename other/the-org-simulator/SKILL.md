---
name: the-org-simulator
description: "Stress-test a proposed org change before announcing it — simulate who gains, who loses, who blocks, where friction erupts in the first 90 days, and run the memo leak test: how does this land when it leaks before you announce it? Use when planning a reorg, changing reporting lines, merging or splitting teams, moving a function, or 'how will this org change land?'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# the-org-simulator

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

Produces a winners/losers map, a friction forecast, the leak-test read, and a sequenced announcement plan.
