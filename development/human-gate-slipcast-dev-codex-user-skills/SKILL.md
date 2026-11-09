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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

