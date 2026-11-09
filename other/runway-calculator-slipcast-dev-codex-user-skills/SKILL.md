---
name: runway-calculator
description: "Calculate cash runway, burn, and the zero-cash date — and whether you're default alive or dead. Use when asked to work out runway, monthly burn, when the money runs out, or how much to raise/cut to reach a target."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# runway-calculator

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

Produces a computed runway summary (net burn, months of runway, zero-cash date, default alive/dead) plus what it takes to extend it.
