---
name: cs-onboard
description: Founder onboarding interview that captures company context across 7 dimensions.
  Invoke with /cs-onboard setup for initial interview or /cs-onboard update for quarterly
  refresh. Generates ~/.claude/company-context.md used by all C-suite advisor skills.
  Use when setting up the C-suite advisors for the first time, or when company context
  is missing or more than 90 days old — e.g. after a fundraise or pivot.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# cs-onboard

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
