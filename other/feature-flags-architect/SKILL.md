---
name: feature-flags-architect
description: Use when adding, retiring, or auditing feature flags. Triggers on "add
  a flag", "ship behind a flag", "rollout plan", "kill switch", "stale flags", "flag
  debt", "LaunchDarkly", "GrowthBook", "Statsig", "Unleash", "Flipt", or any progressive-delivery
  question. Ships flag debt scanner, rollout planner, and kill-switch auditor (all
  stdlib Python), 4 references on flag taxonomy + provider trade-offs + rollout strategies
  + lifecycle, plus a /flag-cleanup slash command.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# feature-flags-architect

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

