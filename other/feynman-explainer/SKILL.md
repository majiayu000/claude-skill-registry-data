---
name: feynman-explainer
description: "Learn something deeply by trying to explain it simply — the Feynman technique — surfacing exactly the gaps where your understanding is fake. Use when asked help me really understand X, explain this back to check my understanding, use the Feynman technique on, or do I actually get this."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# feynman-explainer

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

Produces a prompt to explain the concept in plain language yourself, a check that flags where your explanation went vague, hand-wavy, or jargon-hid a gap, the specific things you don't actually understand yet, and how to close each — because if you can't explain it simply, you don't really know it.
