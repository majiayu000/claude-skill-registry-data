---
name: autopilot-charter
description: "Decide which of your recurring rituals to put on autopilot — and which to keep manual. Use when asked what to automate, how to set up recurring AI runs, which reports or briefings could run on a schedule, or to design an automation charter for a team."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# autopilot-charter

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

Produces a ritual inventory with automate/assist/keep-manual calls, guardrails per ritual, and a rollout order.
