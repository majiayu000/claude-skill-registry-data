---
name: foia-request
description: "Draft a public-records request (FOIA / FOI / state open-records) that's specific enough to get records and hard to deny. Use when asked to write a FOIA request, records request, or freedom-of-information request to a government body."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# foia-request

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

Produces a properly-scoped request: the records sought, date range and format, fee-waiver and expedited-processing asks where applicable, and citations to the governing statute.
