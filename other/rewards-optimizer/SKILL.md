---
name: rewards-optimizer
description: "Figure out the best card or payment route for a purchase (or your everyday spending) to maximize cashback/points — without overspending or drowning in complexity. Use when asked which card should I use for [purchase], maximize my credit card rewards, best card for [category], or optimize my points. Not financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# rewards-optimizer

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

Produces the best-value route for the spend from the cards/programs you actually have, a simple everyday cheat-sheet by category, redemption tips, and honest guardrails (pay in full, don't chase points into debt or clutter).
