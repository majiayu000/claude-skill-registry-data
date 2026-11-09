---
name: ai-workflow-designer
description: "Design an AI-assisted workflow for a recurring task — which steps to hand to AI, which to keep human, and how they connect — so you get leverage without losing quality or control. Use when asked how do I use AI for [process], automate this with AI, design an AI workflow, or where does AI fit in my process."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-workflow-designer

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

Produces a map of the task's steps split into AI-does / human-does / human-checks, the right tool/prompt for each AI step, the hand-offs and review points, the failure modes to guard against, and a start-small rollout — turning a manual process into a reliable AI-assisted one that keeps you in control.
