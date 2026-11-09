---
name: fantasy-league-drafter
description: "Build a fantasy-sports draft strategy and weekly plan that fits your league's exact settings — so you draft with a plan instead of vibes. Use when asked to help with my fantasy draft, who should I draft, fantasy league strategy, or set my lineup this week."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# fantasy-league-drafter

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

Produces a settings-aware draft approach (positional strategy by round, tiers over rankings, targets and values), a snake/auction plan for your slot, weekly start/sit and waiver logic, and honest reminders that player values shift — verify current status before locking anything in.
