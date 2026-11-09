---
name: interrupt-rules
description: "Write the between-brief alert rules for a proactive agent: exactly what may interrupt you, what waits for the next brief, and the wording of an interruption. Use when asked to set interrupt rules, only alert me for X, stop my agent pinging me, decide what counts as urgent for Duet, or define when an AI assistant may break my focus."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# interrupt-rules

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

Produces a short ruleset with named interrupt triggers, a default of silence, quiet hours, and the three-line alert format.
