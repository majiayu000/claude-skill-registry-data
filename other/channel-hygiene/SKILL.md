---
name: channel-hygiene
description: "Fix a team's chat sprawl — the channel map with one purpose per channel, the naming scheme that makes purpose findable, the archive pass for the dead and duplicated, and the posting norms (threads, @-discipline, urgency signals) that keep signal findable. Use when asked clean up our Slack/Teams, we have 90 channels and nothing is findable, set channel norms, or where should things get posted."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# channel-hygiene

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

Produces the channel audit and map, the naming scheme, the norms card, and the archive pass.
