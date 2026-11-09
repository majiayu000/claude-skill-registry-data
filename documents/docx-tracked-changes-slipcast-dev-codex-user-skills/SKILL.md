---
name: docx-tracked-changes
description: "Produce properly-formatted tracked changes for a Word document. Use when asked to redline a document, suggest edits to a contract or document, create tracked changes for review, or mark up a document with proposed revisions. Best used with Claude Opus 4.7 or newer for reliable tracked changes handling."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# docx-tracked-changes

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

Produces a complete redline with insertions, deletions, and margin comments that can be applied to the source document.
