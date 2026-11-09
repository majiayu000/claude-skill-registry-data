---
name: wine-pairing
description: "Pick a wine that flatters tonight's meal — at your budget, from what's actually available — without the sommelier mystique. Use when asked what wine goes with [dish], help me pick a wine, what should I drink with dinner, or recommend a bottle for."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# wine-pairing

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

Produces a couple of specific bottle styles (not just 'a red'), why each works with the dish, a budget-tier pick, an easy-to-find fallback, and a non-alcoholic option — with a plain reason you can remember next time.
