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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
