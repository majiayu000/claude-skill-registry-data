---
name: whats-for-dinner
description: "Decide what to cook tonight from what you already have and how much time/energy you've got — no shopping trip, no recipe rabbit hole. Use when asked what should I make for dinner, what can I cook with what's in my fridge, quick dinner ideas, or I don't know what to eat."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# whats-for-dinner

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

Produces 3 doable options ranked by effort with a quick method for each, honest substitutions, and a 'need one thing' flag if a near-miss is worth a corner-shop run — respecting diets and dislikes.
