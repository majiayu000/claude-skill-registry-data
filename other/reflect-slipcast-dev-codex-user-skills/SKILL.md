---
name: reflect
description: 'Mid-conversation reflection skill that pauses execution and zooms out
  from detail-mode to honestly reassess direction, assumptions, and bias. Use when
  the user says ''reflect'', ''take a step back'', ''step back'', ''zoom out'', ''are
  we missing something'', ''bigger picture'', ''sanity check this'', ''are we on track'',
  ''are we overthinking this'', ''forest for the trees'', or any variation signaling
  intent to break out of detail-mode and reassess. Also trigger when the conversation
  has gone deep on implementation details without strategic check-in, or when the
  user shows signs of being stuck — that''s often a signal the framing needs a reset,
  not more detail work. Intentionally low-intake: runs the 5-dimension analysis immediately
  when prior context is rich enough; asks one forcing clarifier only when invocation
  context is too thin to reassess from.'
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# reflect

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

