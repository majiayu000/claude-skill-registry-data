---
name: ship-or-slip
description: "Turn a release-readiness argument into one typed decision — ship, ship reduced, or slip — with a defined state, defined options, and a probability for each. Use when asked should we ship Friday, are we ready to release, do we slip the date, go/no-go for the release, or when a launch checklist is done and someone still has to call it."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ship-or-slip

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

Produces a filled release state, the three-way decision with probabilities and confidence, the act-or-hold verdict against the thresholds, and the one fact that would flip it.
