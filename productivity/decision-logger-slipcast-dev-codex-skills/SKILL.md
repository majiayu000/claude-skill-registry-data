---
name: decision-logger
description: Two-layer memory architecture for board meeting decisions. Manages raw
  transcripts (Layer 1) and approved decisions (Layer 2). Use when logging decisions
  after a board meeting, reviewing past decisions with /decision-logger decisions,
  or checking overdue action items with /decision-logger review. Invoked automatically
  by the board-meeting skill after Phase 5 founder approval.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# decision-logger

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
