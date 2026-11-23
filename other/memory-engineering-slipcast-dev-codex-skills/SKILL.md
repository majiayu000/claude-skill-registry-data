---
name: memory-engineering
description: Use when designing, reviewing, or paying for an agent memory system —
  adding memory to an agent, choosing between long-context / RAG / graph / agentic
  memory, auditing what a AGENTS.md or memory directory actually holds, deciding what
  to keep and what to expire, or when a memory store keeps growing and nobody has
  said what leaves it. Prices the write path, picks which cost to pay, classifies
  records as facts / skills / logs, and refuses a design that has no forgetting policy.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# memory-engineering

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
