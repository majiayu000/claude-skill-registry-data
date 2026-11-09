---
name: recurring-meeting-pruner
description: "Prune your own recurring-meeting load — the personal calendar audit (your role in each, honestly), the four exit moves (leave, delegate, downgrade to notes, halve), and the graceful exit scripts that don't burn standing. Use when asked get me out of some of these meetings, my calendar is 80% recurring, which meetings can I stop attending, or leave a meeting politely."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# recurring-meeting-pruner

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

Produces the personal audit with role verdicts, the exit move per meeting, the scripts, and the calendar-shape after.
