---
name: fact-check-pass
description: "Run a claim-by-claim fact-check pass on a draft article, script, or report before publication. Use when asked to fact-check a piece, verify claims before publishing, or do editorial verification."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# fact-check-pass

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

Produces a claim inventory (every checkable assertion pulled out), a verification status and source for each (confirmed / needs sourcing / unverifiable / wrong), the fixes, and a flag on the high-risk claims (numbers, quotes, names, legal/defamatory statements) that must not go out unverified.
