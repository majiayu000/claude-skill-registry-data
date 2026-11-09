---
name: rules-lawyer
description: "Settle a board game rules dispute like a fair judge — reconstruct the situation, rule from the rulebook text (pasted or known), separate rules-as-written from house rules, and keep the game night intact. Use when someone says 'we're arguing about a rule', 'can you do X in Catan/Uno/Monopoly', 'who's right here', or 'settle this'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# rules-lawyer

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

Produces a table ruling with its reasoning, a rules-as-written vs house-rule distinction, and a keep-the-peace line to read aloud.
