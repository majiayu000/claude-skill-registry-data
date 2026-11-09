---
name: school-choice-decision
description: "Choose the right school for a specific child by weighing what actually matters to them and your family — not just rankings. Use when asked how to choose a school, compare schools for my kid, which school is best, or help me decide on a school."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# school-choice-decision

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

Produces a priorities profile for this child, a comparison of the options on the factors that matter (fit, teaching, environment, logistics, cost), the questions to ask and things to observe on visits, a weighted decision, and a note that a good fit beats a high ranking.
