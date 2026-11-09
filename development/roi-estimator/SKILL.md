---
name: roi-estimator
description: "Estimate the ROI, payback, and NPV of an investment, project, or purchase. Use when asked to calculate ROI, build a business case, justify a purchase/initiative, work out payback period, or compare options by return."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# roi-estimator

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

Produces a computed ROI summary (net benefit, ROI %, payback, simple NPV) with the assumptions made explicit and a sensitivity note, so a business case is defensible.
