---
name: challenge
description: Pre-mortem plan analysis. Imagine the plan failed 12 months from now
  and work backwards to find the weaknesses. Surfaces assumptions, dependencies, and
  execution risks before committing resources. Use when before significant resource
  commitment, before presenting to a board or investors, when feedback has been one-sidedly
  positive, or when there is pressure to move fast and figure it out later.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# challenge

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

