---
name: promoter-draft
description: "Turn one recurring pattern from a promoter scan into a complete, reusable skill in this library's format: a SKILL.md with a strong trigger description, required inputs, a framework, an output template, quality checks, anti-patterns, and three worked examples derived from the user's real prompts, plus the bundle manifest. Use when asked to draft a skill from this pattern, promote this pattern into a skill, write the SKILL.md for what I keep asking, or as the second step of the promote loop."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# promoter-draft

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

Produces a ready-to-test skill folder that anyone, not just the original user, can use.
