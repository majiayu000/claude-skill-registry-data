---
name: pulse
description: "Multi-source recency research skill that takes the pulse of any topic across Reddit, Hacker News, the open web, and optionally X/Twitter within a configurable recent window (default 30 days). Forcing intake clarifies topic specificity, angle (trend/sentiment/problems/opportunities/comparison), time window, and platform scope before searching. Use when the user requests multi-source recency intelligence on a topic (e.g., 'pulse on [topic]', 'what's happening with [topic]', 'what are people saying about [topic]', 'current conversation about [topic]', 'take the pulse of [topic]', 'trending: [topic]', 'find me info on [topic]'), and for competitor research, trend discovery, tool comparisons, and audience sentiment analysis."
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# pulse

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

Returns a synthesized briefing with citations, engagement metrics, and cross-platform pattern analysis.
