---
name: research
description: Default entry point for any research request — a hybrid router that classifies
  the question deterministically and either delegates to a specialist research skill
  (pulse for trends/sentiment, grants for NIH funding, litreview for academic literature,
  syllabus for course reading, patent for prior-art + IP landscape, dossier for entity
  research, deepread for evidence-first reading of supplied documents) or runs its
  own plan-decompose-multi-source-search-synthesize-cite fallback workflow when no
  specialist matches. Always surfaces the routing decision so users can override.
  Use when the user makes any research request that doesn't obviously match a more-specific
  specialist skill (e.g., "research [topic]", "look into [topic]", "what do we know
  about [topic]", "investigate [topic]", "find me information on [topic]", "do some
  research on [topic]", "I need to understand [topic]").
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# research

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

