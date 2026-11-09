---
name: beneficiary-audit
description: "Audit the beneficiary designations that quietly override wills — the account-by-account sweep, the life-event triggers that make them stale, and the coordination check against actual intentions. Use when asked check my beneficiaries, does my 401k go to my ex, do beneficiary forms beat a will, or what should I update after marriage/divorce/a birth."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# beneficiary-audit

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

Produces the account sweep list, the stale-designation red flags, the intent-vs-paperwork comparison table, and the update checklist with the verify-in-writing step.
