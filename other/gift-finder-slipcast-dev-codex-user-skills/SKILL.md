---
name: gift-finder
description: "Find a genuinely good gift for a specific person and occasion within a budget — thoughtful and non-obvious, not a generic 'top 10 gifts' list. Use when asked for gift ideas, what should I get [person], help me find a present, or I have no idea what to buy."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# gift-finder

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

Produces a short set of tailored ideas across price points, why each fits this person, where to get it and rough price, a safe backup, and an honest flag when you need one more detail to nail it.
