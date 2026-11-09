---
name: aeo-optimizer
description: "Optimize an article for Answer Engine Optimization (AEO) so AI engines like ChatGPT, Perplexity, and Claude can extract, quote, and cite it. Use when asked to AEO-optimize, make content AI-readable, improve AI citation chances, or adapt an article for answer engines."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# aeo-optimizer

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

Produces an AEO-optimised rewrite with question headings, 50–80 word answer capsules, a paragraph-length audit, and flagged trust signals.
