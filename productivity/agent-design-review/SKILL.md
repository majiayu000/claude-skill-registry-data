---
name: agent-design-review
description: "Review an LLM agent design and find where it will be unreliable, expensive, or unsafe. Use when asked to review an agent architecture, critique a multi-step/tool-using agent, debug an agent that loops or goes off-task, or harden an agent before launch."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-design-review

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

Produces a structured review — task fit, control flow, tools, memory/context, failure handling, cost, and safety — with prioritised findings and fixes.
