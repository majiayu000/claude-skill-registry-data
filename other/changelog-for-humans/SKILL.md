---
name: changelog-for-humans
description: "Write changelogs and release notes readers actually benefit from — changes translated to so-whats, grouped by reader impact (breaking first, gifts second, plumbing last), with the upgrade path stated and the marketing kept honest. Use when asked write the release notes, turn this commit list into a changelog, announce this update to users, or why does nobody read our changelogs."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# changelog-for-humans

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

Produces the impact-grouped changelog, the so-what translations, the breaking-changes block with migration steps, and the two-audience split when needed.
