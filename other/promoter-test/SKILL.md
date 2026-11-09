---
name: promoter-test
description: "Generate an evals file for a drafted skill and measure whether its trigger description fires on the right requests: five to eight phrases that should trigger it, five that should not, three golden input and output pairs, then precision and recall against the description, with a rewrite loop when precision is below 0.8. Use when asked to test this skill's triggers, write evals for the new skill, check the description fires correctly, or as the third step of the promote loop."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# promoter-test

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

Produces an evals.json beside the skill, a case in the library's evals, and a precision and recall report.
