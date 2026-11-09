---
name: funeral-pricing-decoder
description: "Decode a funeral home price list while grieving — the package maths versus the itemised list, the non-declinable basic fee, the upsells that arrive as care, and the direct-cremation benchmark that anchors every other number. Use when asked to compare funeral quotes, is this funeral price fair, what can we decline, or help me read this price list. Consumer information, not legal advice; disclosure rules are strongest in the US (FTC Funeral Rule)."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# funeral-pricing-decoder

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

Produces a line-by-line decode, the decline-safely list, package-versus-itemised maths, questions for the director, and a comparison across homes.
