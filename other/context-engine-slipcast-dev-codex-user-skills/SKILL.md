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
