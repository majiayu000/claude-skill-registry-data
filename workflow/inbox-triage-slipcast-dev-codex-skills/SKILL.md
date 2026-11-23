---
name: inbox-triage
description: Runs a full inbox triage using the knowledge base created by the 'inbox-setup'
  skill. Light-intake by design (most invocations skip questions and run with KB-default
  preferences); asks at most 2 grill-me override questions when invocation is outside
  normal cadence or includes category-skip intent. Searches recent emails, classifies
  them via the user's taxonomy, researches new senders, generates recommendations,
  drafts replies (NEVER sends), delivers a report in the user's preferred format,
  and updates the knowledge base with learnings. Designed to run on a recurring schedule
  (1-3x daily) or on demand. Use when the user wants their inbox processed, in any
  variation (e.g., 'triage my inbox', 'inbox triage', 'check my email', 'run email
  triage', 'process my inbox', 'what's new in my email', 'handle my email', 'email
  triage'). Requires the inbox-setup skill to have been run first.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# inbox-triage

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

