---
name: agent-project-file
description: "Set up the project file an AI agent keeps for work that runs over days or weeks: the goal, the definition of done, milestones, the current state, decisions made, open questions, and the exact point to resume from after an interruption. Use when asked to plan a long-running agent task, make my agent work on this over a week, keep state between agent sessions, or hand a multi-day project to an AI."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-project-file

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

Produces the project file, the update rules, the check-in schedule and the resume checklist.
