---
name: data-retention-policy
description: "Build a data retention and deletion schedule grounded in legal basis. Use when asked to create a data retention policy, set retention periods, plan data deletion/minimisation, or answer 'how long can we keep this data?'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# data-retention-policy

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

Produces a retention schedule — data categories with their retention period, legal/business basis, deletion trigger and method, plus flags for data kept with no basis or no defined period.
