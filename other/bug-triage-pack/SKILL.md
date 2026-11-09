---
name: bug-triage-pack
description: "Triage a raw bug report into something a team can act on — clean repro steps, a defensible severity/priority, environment, likely area/owner, and duplicate check. Use when asked to triage this bug, set severity and priority, is this a P1, or clean up this bug report for the backlog."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# bug-triage-pack

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

Produces the normalized repro, a severity and priority with the reasoning (impact × frequency × workaround), the environment/metadata, a suspected component and owner queue, and a duplicate/related-issue check — flagging when info is missing rather than guessing.
