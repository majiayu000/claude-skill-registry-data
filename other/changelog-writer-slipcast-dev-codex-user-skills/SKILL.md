---
name: changelog-writer
description: "Turn a list of changes, commits, or PRs into clean release notes / a changelog entry. Use when asked to write release notes, a changelog, or a version announcement from raw changes. To go straight from a raw git log use changelog-generator instead."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# changelog-writer

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

Produces a Keep-a-Changelog-style entry grouped by type (Added/Changed/Fixed/etc.), written for users — surfacing breaking changes and upgrade notes up top.
