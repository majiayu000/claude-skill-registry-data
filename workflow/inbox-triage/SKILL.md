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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

