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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

