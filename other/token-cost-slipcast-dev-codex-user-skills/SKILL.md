---
name: token-cost
description: "Measure before optimizing — estimate token counts locally with stated heuristics, price them at your model's rates, and quantify before/after savings, because token optimization without measurement is vibes. Use when asked how many tokens is this, what does this context cost per call, is this optimization worth it, or compare these two versions' cost."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# token-cost

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

Produces the estimate with both heuristics shown, the cost math at your prices across your call volume, and the before/after comparison that decides whether an optimization earned its complexity.
