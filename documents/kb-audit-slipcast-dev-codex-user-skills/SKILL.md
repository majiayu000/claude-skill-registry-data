---
name: kb-audit
description: "Audit a knowledge base / help center for coverage, accuracy, and findability. Use when asked to audit a help center, review KB health, find documentation gaps, reduce ticket volume with better docs, or prioritise what to write/fix."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# kb-audit

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

Produces an audit — a health scorecard, content gaps (driven by top ticket drivers), stale/duplicate/low-findability articles, and a prioritised fix-and-create backlog.
