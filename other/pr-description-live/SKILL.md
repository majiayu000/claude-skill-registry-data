---
name: pr-description-live
description: Write a PR description grounded in the REAL diff — read the branch's
  actual changes via the GitHub connector, not a template the user fills in. Use when
  asked to write my PR description, describe this pull request, draft the PR body
  from my branch, or document these changes in Cowork. Reads the commits and diff
  via the GitHub connector, derives what changed and why from the code itself, and
  produces a PR-description artifact (summary, changes, testing, risk) ready to paste
  — matching the repo's PR template if one exists.
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# pr-description-live

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

