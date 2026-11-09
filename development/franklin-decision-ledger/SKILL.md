---
name: franklin-decision-ledger
description: "Run a hard two-option decision through Benjamin Franklin's 'moral or prudential algebra' — the weighted pro/con method he described to Joseph Priestley in 1772 — including the part everyone skips: striking out reasons that cancel, and letting the ledger sit before deciding. Use when weighing job offers, relocations, build-vs-buy, take-the-promotion, shut-it-down decisions, or any 'I keep going back and forth'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# franklin-decision-ledger

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

Produces a completed decision ledger with a leaning, its strongest counter, and a revisit date.
