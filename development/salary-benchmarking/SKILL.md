---
name: salary-benchmarking
description: "Build a defensible salary range for a role — what it actually pays given the market, location, level, and your value — so you can ask, counter, or set pay with a real number. Use when asked what should I be paid, is my salary fair, research market pay for [role], or how much to ask for. Not the same as running the negotiation."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# salary-benchmarking

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

Produces a structured way to research the range from multiple sources, the factors that move your number (level, location, industry, skills, company size), where you likely sit in the band, and how to frame the number — flagging that pay data varies and should be triangulated, not taken from one source.
