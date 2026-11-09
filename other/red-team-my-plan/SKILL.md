---
name: red-team-my-plan
description: "Attack your own plan the way a smart adversary would — find the weakest point, the thing you're hoping nobody notices, and where it breaks under pressure. Use when asked to red-team this, attack my plan, find the holes, or where does this break."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# red-team-my-plan

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

Produces an adversarial breakdown of the plan's weakest points, the single move an opponent (or reality) would make to break it, the part you're quietly hoping holds, and the fixes that close the biggest gaps — a hostile stress-test done by your own side, before someone else does it for real.
