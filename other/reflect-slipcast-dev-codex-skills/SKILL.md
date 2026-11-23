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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

