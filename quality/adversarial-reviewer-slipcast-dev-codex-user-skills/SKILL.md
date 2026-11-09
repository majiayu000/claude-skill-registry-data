---
name: adversarial-reviewer
description: Adversarial code review that breaks the self-review monoculture. Use
  when you want a genuinely critical review of recent changes, before merging a PR,
  or when you suspect Claude is being too agreeable about code quality. Forces perspective
  shifts through hostile reviewer personas that catch blind spots the author's mental
  model shares with the reviewer.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# adversarial-reviewer

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

