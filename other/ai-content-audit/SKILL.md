---
name: ai-content-audit
description: "Audit a content library, docs site, or blog for AI-generated filler that's eroding trust and search performance — and triage what to fix, rewrite, or delete. Use when asked to find slop in a content library, audit AI-written content quality, explain why content engagement or rankings dropped after scaling with AI, or set a quality bar for AI-assisted publishing. For a single article's AI-citability use aeo-optimizer; for the strategy itself use content-calendar or seo-content-brief."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-content-audit

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

Produces an audited inventory with per-piece verdicts, the detection signals used, a triage plan, and a publishing quality gate that prevents recurrence.
