---
name: benefits-cliff-check
description: "Check whether a raise, more hours, or a new job could cost you more in lost benefits than you gain — the 'benefits cliff' — before you accept it. Use when asked will a raise hurt my benefits, benefits cliff, if I make more will I lose my food stamps or medicaid, or should I take more hours. Not financial/benefits advice; points to a benefits counselor."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# benefits-cliff-check

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

Produces a plain map of which benefits phase out at what income (and which cut off suddenly vs. taper), a rough read on whether a specific income change helps or hurts net, the ones with hard cliffs to watch (childcare, Medicaid, housing), the moves that soften a cliff, and where to get a real benefits screening.
