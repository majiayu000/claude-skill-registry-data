---
name: backup-strategy
description: "Set up a backup system that actually protects your photos, files, and devices — built on the 3-2-1 rule and, crucially, tested so it works when you need it. Use when asked how to back up my data, set up backups, protect my photos/files, or what's a good backup strategy."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# backup-strategy

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

Produces a 3-2-1 plan tailored to your devices and data, specific what-to-back-up priorities, an automation setup so it happens without you, a restore-test step, and protection against the failure that ruins backups (ransomware/sync-deletes reaching the backup).
