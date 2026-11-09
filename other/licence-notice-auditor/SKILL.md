---
name: licence-notice-auditor
description: "Use when asked to check a project's licences, audit dependencies before open-sourcing or selling, write a NOTICE file, find licence conflicts, or check whether bundled fonts, images or datasets can be shipped."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# licence-notice-auditor

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

Produces an inventory of code, data and media dependencies with their licences, flags for conflicts and unclear ownership, and a draft NOTICE.md, with a clear statement that the output is not legal advice.
