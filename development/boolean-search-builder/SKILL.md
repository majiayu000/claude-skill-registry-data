---
name: boolean-search-builder
description: "Build boolean and X-ray search strings to source candidates. Use when asked to build a boolean search, source candidates on LinkedIn/Google, write an X-ray search, or find people with specific skills."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# boolean-search-builder

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

Produces ready-to-paste boolean strings (with synonyms, must-haves, and exclusions), X-ray variants for LinkedIn/GitHub, and a refinement plan to widen or narrow the result set.
