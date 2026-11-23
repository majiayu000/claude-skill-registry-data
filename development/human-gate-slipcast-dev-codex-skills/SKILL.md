---
name: human-gate
description: Runs the human-verification lane of an agent loop, and proves review
  happened before work is called done. Builds a single-file HTML review page, collects
  batched feedback as a structured artifact instead of chat prose, and runs a gate
  that refuses to close while a BLOCKER is open, the reviewer is unnamed, or nobody
  has reviewed at all. Use when a plan, spec, RFC, report, landing page, migration,
  or any irreversible action needs human sign-off before shipping, or on requests
  such as 'get sign-off', 'have someone check this', 'hold until reviewed', 'needs
  approval first'. NOT for making AI text sound human (use content-humanizer or behuman).
  NOT for reviewing code diffs (use md-review or code-reviewer).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# human-gate

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

