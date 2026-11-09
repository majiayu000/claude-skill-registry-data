---
name: the-understudy
description: "Study 3-5 samples of the user's real writing and decisions, build an explicit 'how you think' profile, then draft new work as their understudy — always with a 'what I couldn't infer about you' list so the gaps are visible instead of guessed. Use when someone says 'write it like I would', 'learn my style', 'draft this as me', or wants an AI that apprentices to their judgment rather than imitating their tone."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# the-understudy

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

Produces a thinking profile, an understudy draft, and the couldn't-infer list.
