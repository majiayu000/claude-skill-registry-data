---
name: ambiguity-resolver
description: "Structure vague opportunities and unclear briefs into actionable one-page problem statements. Use when asked to clarify a vague brief, frame an undefined problem, make sense of an unclear opportunity, or when the user says 'we need to figure out what to do about X' or 'I've been asked to look into Y'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ambiguity-resolver

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

Produces a structured problem brief with reframed questions, scoped boundaries, and a minimum viable research plan.
