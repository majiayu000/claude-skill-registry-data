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
