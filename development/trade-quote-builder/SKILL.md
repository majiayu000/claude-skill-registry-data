---
name: trade-quote-builder
description: "Build a trade quote that wins the job and protects the margin — materials and labor itemized, assumptions and exclusions stated, variations priced by rule, and the professional one-page layout customers trust. Use when a tradesperson says 'help me quote this job', 'I keep losing money on jobs', 'customer wants a price for X', or 'how do I quote a day rate vs fixed'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# trade-quote-builder

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

Produces a ready-to-send quote plus the internal costing sheet behind it.
