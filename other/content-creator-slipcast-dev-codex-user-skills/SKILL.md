---
name: content-creator
description: Deprecated redirect skill that routes legacy 'content creator' requests
  to the correct specialist. Use when a user invokes 'content creator', asks to write
  a blog post, article, guide, or brand voice analysis (routes to content-production),
  or asks to plan content, build a topic cluster, or create a content calendar (routes
  to content-strategy). Does not handle requests directly — identifies user intent
  and redirects to content-production for writing/SEO/brand-voice tasks or content-strategy
  for planning tasks.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# content-creator

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

