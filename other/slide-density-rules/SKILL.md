---
name: slide-density-rules
description: "Fix slides that are documents in landscape mode — the one-point-per-slide rule, the projection-vs-reading fork that decides density, the text diet (headlines and evidence, prose to notes), and the glance test. Use when asked my slides are too busy, how much text per slide, fix this wall-of-bullets deck, or make this readable from the back of the room."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# slide-density-rules

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

Produces the density diagnosis, the per-slide fixes (split, strip, or move-to-notes), the projection/document fork decision, and the glance-test results.
