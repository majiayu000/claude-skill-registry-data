---
name: voting-navigator
description: "Work out how to actually vote in a specific election — am I registered, what's the deadline, how do I vote (in person / mail / early), what ID do I need, and what's on my ballot — with everything routed to the official source to verify. Use when someone says 'how do I vote', 'am I registered', 'what's the deadline to register', 'help me vote by mail', or 'what's on my ballot'. Non-partisan; procedure only, never who to vote for."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# voting-navigator

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

Produces a personal voting plan with dates, steps, and the official links to confirm each one.
