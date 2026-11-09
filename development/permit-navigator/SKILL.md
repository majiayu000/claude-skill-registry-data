---
name: permit-navigator
description: "Work out which permits a project actually needs and the order to get them — building/renovation, business licensing, events, signage, home businesses — so you don't build first and discover the permit later. Use when someone says 'do I need a permit for this', 'what permits for my renovation/business/event', 'help me apply for a permit', or 'the council flagged my project'. Not legal/code advice — it orients and routes to the authority."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# permit-navigator

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

Produces a permit checklist with the likely permits, their sequence and dependencies, and the official offices to confirm each.
