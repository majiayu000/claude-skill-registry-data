---
name: idea-storm
description: "Generate a big, wide spread of ideas for anything by running the prompt through many different lenses at once, then clustering and picking. Use when asked to brainstorm ideas for, give me lots of options, help me come up with, or I need ideas for."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# idea-storm

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

Produces a high-volume, deliberately varied idea list generated across multiple angles (safe, wild, cheap, ambitious, weird, opposite), grouped into themes, and a shortlist of the most promising — maximizing range so you're not choosing from three obvious options.
