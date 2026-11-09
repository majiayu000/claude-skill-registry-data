---
name: life-premortem
description: "Write the failure story of your year, relationship, move, or big life bet in advance — imagine it's a year later and it went wrong, tell that story vividly, then mine it for the real risks and the cheap things that would have prevented them. Use when someone says 'I'm about to make a big life change', 'what could go wrong with this', 'de-risk my year', or is committing to something large and irreversible. The life-scale sibling of a project premortem."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# life-premortem

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

Produces the failure narrative, the extracted risk list with preventatives, and the early-warning signs to watch.
