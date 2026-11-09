---
name: promoter-publish
description: "Register a finished skill in this library and produce the complete release package: the bundle wiring and marketplace entry, the regenerated catalogue and exports, the headline count in every living document, the CHANGELOG entry, the gates to run, and the exact git and release commands. Use when asked to publish this skill, release the new skill, add it to the marketplace, ship the promoted skill, or as the last step of the promote loop."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# promoter-publish

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

Produces the full release package, never a partial one, with a confirmation step before anything is pushed.
