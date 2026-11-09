---
name: ev-vs-gas
description: "Compare an EV against a comparable gas car on total cost — upfront gap after incentives, energy vs fuel per year, maintenance delta, and the crossover year when the EV pulls ahead (or doesn't). Use when asked is an EV worth it, EV vs gas total cost, when does an EV pay for itself, or should my next car be electric."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ev-vs-gas

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

Produces the year-by-year cumulative comparison from the script, the crossover year, the per-mile energy math, and the honest not-modeled list.
