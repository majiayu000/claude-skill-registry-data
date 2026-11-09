---
name: metric-gaslighting-detector
description: "Find out how a dashboard, KPI report, or metrics slide is lying to you — before you repeat its story in a bigger room. Use when numbers feel too tidy, a narrative rests on one chart, or you inherited metrics you didn't define."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# metric-gaslighting-detector

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

Produces a deception audit: every metric graded for the eleven classic distortions (denominator games, survivorship, y-axis crimes, cherry-picked windows…), the story the data would tell under honest framing, and the three questions to ask the metric's owner.
