---
name: agenda-or-cancel
description: "Enforce the simplest meeting rule that works — no agenda, no meeting — with the three-line agenda format (purpose, decisions sought, pre-reads), the 24-hour rule, and the graceful cancel scripts. Use when asked write an agenda for this meeting, should this meeting happen, our meetings have no agendas, or cancel this meeting politely."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agenda-or-cancel

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

Produces the three-line agenda, the happen-or-cancel verdict, the cancel/convert scripts, and the team norm rollout.
