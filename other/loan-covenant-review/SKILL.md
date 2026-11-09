---
name: loan-covenant-review
description: "Run a quarterly loan covenant compliance review: covenant table with required vs actual vs headroom, trend and trajectory-to-breach analysis, waiver and amendment options with pricing implications, early-warning indicators, and a watch-list recommendation. Use when asked to review covenant compliance, check covenant headroom, assess a potential covenant breach, or prepare a quarterly borrower monitoring review."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# loan-covenant-review

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

Produces a structured covenant review with headroom table, trajectory analysis, and recommended actions.
