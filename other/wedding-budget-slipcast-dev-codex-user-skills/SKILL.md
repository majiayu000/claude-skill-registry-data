---
name: wedding-budget
description: "Build a wedding budget that survives to the wedding — allocation by real shares, the per-guest lever made explicit, the routinely-forgotten line items priced in from day one, and a contingency that isn't decorative. Use when asked make a wedding budget, how do people split X across a wedding, we have N dollars and M guests, or why is our wedding over budget."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# wedding-budget

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

Produces the allocation table from the script, the guest-count math, the forgotten-items audit, and the track-against-actuals discipline.
