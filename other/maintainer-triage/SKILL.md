---
name: maintainer-triage
description: "Get an open-source repo's issue backlog from 400-and-drowning to triaged-and-honest in one pass — a label taxonomy that encodes decisions, batch triage rules you can apply in seconds per issue, saved replies that stay kind at scale, and stale-bot policy set with a conscience. Use when a maintainer says 'my issues are out of control', 'triage my backlog', 'set up labels for my repo', or dreads opening GitHub."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# maintainer-triage

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

Produces the taxonomy, the triage pass rules, saved replies, and a sustainable weekly routine.
