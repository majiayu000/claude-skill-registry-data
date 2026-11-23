---
name: context-engine
description: Loads and manages company context for all C-suite advisor skills. Reads
  ~/.claude/company-context.md, detects stale context (older than 90 days), enriches
  context during conversations, and enforces privacy/anonymization rules before external
  API calls. Use when starting any C-suite advisor session, when context looks stale
  or missing, or before sending company data to an external service.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# context-engine

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
