---
name: wiki-summary
description: "Fetch Wikipedia's current summary of any topic with zero API keys — the REST summary endpoint via curl, for answers that need today's article rather than training-data memory. Use when asked what does Wikipedia say about X, get me the current summary of a topic, check a fact against Wikipedia, or has this article changed."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# wiki-summary

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

Produces the live extract with the article link, disambiguation handling, and a clean separation between what Wikipedia says and what the model adds.
