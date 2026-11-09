---
name: rubric-builder
description: "Create a clear grading rubric with criteria and performance-level descriptors that make scoring fair, fast, and consistent. Use when asked to build a rubric, create grading criteria, design an assessment scoring guide, or make grading more objective."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# rubric-builder

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

Produces an analytic rubric table (criteria × performance levels) with concrete, observable descriptors and a points scheme — plus a short version students can self-check against.
