---
name: evidence-lock
description: "Write or rewrite a document in evidence-locked mode: no unsourced sentences — every substantive claim carries a footnote citing the exact passage in the user's provided sources, and anything unsupportable is explicitly marked. Use when asked to make a document fully sourced, add citations from my docs, ground a draft in the attached material, or produce something for audiences that will check (legal, board, regulators, enterprise buyers)."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# evidence-lock

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

Produces the document with numbered citations, a source map quoting each cited passage, and an unsupported-claims register.
