---
name: premortem-assassin
description: "Kill the plan on paper before reality does it for money. Use when a plan, launch, migration, or strategy is about to be committed to and nobody has tried hard to murder it yet — the assassin attacks through twelve named failure vectors and writes the post-mortem of the failure that hasn't happened."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# premortem-assassin

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

Produces a premortem: the death narrative, the twelve-vector attack with survival verdicts, the three kill-shots most likely to land, and the cheap tripwires that would give early warning.
