---
name: data-broker-removal
description: "Get your personal info off people-search and data-broker sites — a prioritized opt-out plan that targets the sites that matter and keeps them from reappearing. Use when asked to remove my info from the internet, opt out of data brokers, my address/phone is on people-search sites, or reduce my digital footprint."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# data-broker-removal

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

Produces a prioritized target list (the high-traffic brokers first), the opt-out method for each, a suppression-at-source plan so data stops flowing back, a recheck cadence, and safe-handling cautions for the personal data you'll be submitting.
