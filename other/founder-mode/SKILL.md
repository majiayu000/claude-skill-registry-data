---
name: founder-mode
description: /c-level-agents:founder-mode [question] — Auto-routes any founder question
  to the right C-role advisor or to /c-level-agents:boardroom for multi-role topics.
  The single-command entry point. Use when a founder asks any strategic question without
  knowing which advisor or command fits — e.g. 'runway pressure' routes to the CFO,
  'gross retention dropped' routes to the CCO.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# founder-mode

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
