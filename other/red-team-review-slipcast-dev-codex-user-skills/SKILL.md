---
name: red-team-review
description: "Stress-test a plan, strategy, PRD, or launch by simulating hostile expert personas who attack it from every angle. Use when asked to red-team, stress-test, pre-mortem, pressure-test, play devil's advocate, or find the blind spots in a plan before committing."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# red-team-review

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

Produces a per-persona critique, a ranked list of the most dangerous risks, a pre-mortem, and the specific changes that would most strengthen the plan.
