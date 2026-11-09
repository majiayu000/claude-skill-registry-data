---
name: async-standup-compiler
description: Compile the team's REAL updates into one async standup — pull what people
  posted in Slack (and moved in Notion/Linear), not a template for running standups.
  Use when asked to compile today's standup, pull the team's updates into one post,
  what did the team ship, or run async standup in Cowork. Reads a Slack channel and
  (optionally) the tracker via connectors, groups updates by person into shipped /
  in-progress / blocked, surfaces the blockers needing attention, and produces a standup-digest
  artifact ready to post back.
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# async-standup-compiler

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

