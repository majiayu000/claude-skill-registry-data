---
name: make-me-a-skill
description: "Turn a task you repeat every week into a reusable personal skill or prompt — so you say 'do this' instead of re-explaining it every time. Use when asked help me make a skill for, turn this repetitive task into a template, I do this every week, or create a reusable prompt for this."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# make-me-a-skill

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

Produces a captured spec of the repetitive task (its inputs, steps, and what good output looks like), a reusable skill/prompt you can invoke by name, and guidance on saving and refining it — lowering the barrier from AI user to AI author, one weekly task at a time.
