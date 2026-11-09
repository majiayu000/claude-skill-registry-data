---
name: good-enough-detector
description: "Tell you when to stop polishing and ship — the point where more effort stops adding real value. Use when asked is this good enough, should I keep working on this, when do I stop, or I keep tweaking this and can't let go."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# good-enough-detector

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

## Требования к результату

Produces a read on whether the thing already meets its actual bar, the diminishing-returns check (is more effort improving it or just moving it around), what genuinely still needs fixing vs what's perfectionism, and a clear ship / one-more-pass / keep-going verdict — freeing you from polishing things past the point anyone will notice.
