---
name: standing-meeting-audit
description: "Audit the recurring meetings a team has accreted — each standing slot tested against its original purpose, current attendance reality, and outcomes, with keep/shrink/merge/kill verdicts and the two-week cancellation experiment that settles arguments. Use when asked audit our recurring meetings, our calendar is all standing syncs, which meetings should die, or reset the team's meeting load."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# standing-meeting-audit

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

Produces the inventory with per-meeting verdicts, the experiment protocol, the merge map, and the re-accretion guard.
