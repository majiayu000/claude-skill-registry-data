---
name: pricing-sensitivity-model
description: "Van Westendorp price sensitivity, computed from real survey answers — crossings found by interpolation, not read off a chart by eye. Use when someone has (or plans) the four-question pricing survey (too cheap / cheap / expensive / too expensive) and needs the optimal price point, the acceptable range, and a defensible readout."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# pricing-sensitivity-model

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

Produces OPP/IPP and the PMC–PME range, the four cumulative curves as data, and a real .xlsx with a live revenue what-if — via the bundled zero-dependency script.
