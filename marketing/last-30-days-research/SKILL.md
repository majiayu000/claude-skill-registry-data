---
name: last-30-days-research
description: "Searches Reddit, X/Twitter, and the broader web for recent opinions, sentiment, and signal on any topic. Use when you need to know what real people are saying about a tool, product, trend, or event in the past 30 days — cutting through SEO content to surface genuine community reaction."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# last-30-days-research

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

Produces a structured report with consensus findings, pain points, positive signals, contrarian takes, source links, and a signal confidence rating.
