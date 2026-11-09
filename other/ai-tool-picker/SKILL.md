---
name: ai-tool-picker
description: "Figure out which AI tool actually fits the task in front of you — chatbot, coding assistant, image model, agent, or none — instead of forcing one tool onto everything. Use when asked which AI tool should I use for, what's the best AI for, do I even need AI for this, or should I use ChatGPT or something else."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ai-tool-picker

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

Produces a match between your task and the right kind of AI tool (with why), the trade-offs that matter for your case, when the answer is a non-AI tool or plain human effort, and how to try it cheaply before committing — so you pick by fit, not by hype or habit.
