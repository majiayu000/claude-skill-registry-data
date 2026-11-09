---
name: technical-debt-register
description: "Document and prioritize a technical debt backlog with business impact, effort estimates, and resolution strategy. Use when asked to audit technical debt, create a debt register, prioritize tech debt for a quarter, document architectural shortcuts, or build a debt reduction roadmap."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# technical-debt-register

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

Produces a structured technical debt register covering debt inventory by category, business impact per item, effort and priority scores, top-item resolution plans, and a quarterly debt reduction roadmap.
