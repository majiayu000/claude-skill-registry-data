---
name: altitude-shifter
description: "Re-pitch one piece of content for four audiences — the board, the engineers, a customer, a new hire — with a delta table showing what changed between altitudes and why. Use when asked to rewrite this for execs, explain this to the team, make this customer-facing, or say this four ways."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# altitude-shifter

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

Produces the four versions plus the delta table of what was cut, added, and reframed per altitude.
