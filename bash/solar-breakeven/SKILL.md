---
name: solar-breakeven
description: "Model whether solar panels pay for themselves for your roof — net cost after incentives, bill offset with degradation, electricity inflation, the inverter replacement, and the breakeven year, plus the policy risk no calculator controls. Use when asked are solar panels worth it, when does solar break even, check this solar quote's payback claim, or model solar for my bill."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# solar-breakeven

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

Produces the year-by-year table from the script, the breakeven year, the quote-vs-model comparison, and the not-modeled list led by net-metering risk.
