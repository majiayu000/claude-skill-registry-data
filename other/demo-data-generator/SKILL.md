---
name: demo-data-generator
description: "Use when asked to create demo data, seed a no-signup demo, generate fake but realistic data for screenshots, or fill a sandbox without using real customer data."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# demo-data-generator

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

Produces realistic, internally consistent fake data so a project can ship a demo nobody has to sign up for: a data schema summary, a seeded generation script, seed files, and a checklist confirming no real personal data is included.
