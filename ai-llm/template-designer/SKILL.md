---
name: template-designer
description: "Turn a document the team keeps rewriting into a template that actually helps — extract the recurring skeleton, mark what varies with real placeholder prompts, keep it lighter than the ceremony it replaces, and pilot it before decreeing it. Use when asked make a template from this doc, we write this same thing every week, standardize our status updates or briefs, or why does nobody use our templates."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# template-designer

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

Produces the extracted template with prompting placeholders, the keep-it-light rules, the example-filled twin, and the adoption path.
