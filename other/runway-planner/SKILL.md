---
name: runway-planner
description: "Turn burn and cash into a clear runway picture and a raise decision — months left, default-alive vs default-dead, and what to cut or change. Use when asked to calculate runway, model burn rate, decide when to raise, figure out if the company is default-alive, or plan a scenario with hiring/cuts. Not financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# runway-planner

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

Produces the runway math, a default-alive verdict, and dated trigger points for raising or acting.
