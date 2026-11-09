---
name: changelog-from-commits
description: Write a human changelog from the REAL commit history — read the actual
  commit range via the GitHub connector, not a template. Use when asked to write the
  changelog for this release, what changed since the last tag, draft release notes
  from my commits, or summarise this range for users in Cowork. Reads commits/PRs
  between two refs via the GitHub connector, groups them into user-facing changes
  (features / fixes / breaking), translates commit-speak into human benefit, and produces
  a changelog artifact ready for the release.
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# changelog-from-commits

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

