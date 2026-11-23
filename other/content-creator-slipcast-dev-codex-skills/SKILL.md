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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

