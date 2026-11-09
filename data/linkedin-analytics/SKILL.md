---
name: linkedin-analytics
description: Use when someone wants to understand their own LinkedIn numbers — which
  posts worked, why reach dropped, whether a pattern is real, or how to test a hypothesis.
  Triggers on "why did my reach drop", "what's working on my LinkedIn", "analyze my
  posts", "do carousels do better for me", "should I test this", "LinkedIn analytics".
  Reads your own exported post data, reports medians and outlier bands, tests candidate
  patterns against a permutation null, and sizes a real experiment — refusing to conclude
  anything below 10 posts.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# linkedin-analytics

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

