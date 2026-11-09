---
name: replica-diff
description: 'Compares an app clone against the original: a feature parity score from
  the feature matrix (weighted by must, should, could) with the missing list in build
  order, plus a screenshot layout diff that ignores colour so a rebrand does not count
  against you. Two standard-library Python tools. Use when the user says "how close
  is my clone", "compare it to the original", "what''s missing", "parity check", "diff
  the screens", "is it ready", or after /replica-test.'
metadata:
  source-package: replica-skill-main
  adapted-for: Codex
---

# replica-diff

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

