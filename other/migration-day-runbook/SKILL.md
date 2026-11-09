---
name: migration-day-runbook
description: "Move a team's files to a new platform without losing work or a week — the pre-migration freeze, the verified copy, the permissions remap, the cutover announcement, and the old-system read-only afterlife. Use when asked we're moving from Dropbox to Drive, migrate our files to SharePoint, plan the file migration day, or how do we switch platforms safely."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# migration-day-runbook

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

Produces the migration runbook: freeze window, copy-and-verify steps, permissions mapping, the cutover comms, and the rollback line.
