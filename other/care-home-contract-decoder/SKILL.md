---
name: care-home-contract-decoder
description: "Decode a care-home contract before a parent moves in — the fee-escalation clause with no cap, the needs-can-no-longer-be-met eviction trigger, the guarantor line that quietly makes you personally liable, and the after-death charges nobody mentions on the tour. Use when asked to review a care-home or nursing-home contract, what does this admission agreement mean, can they raise the fees, or can they make my parent leave. Pairs with long-term-care-options for choosing the home; this is for the contract. Not legal advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# care-home-contract-decoder

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

Produces a clause-by-clause decode ranked by financial and eviction risk, the questions to put in writing before signing, and the negotiate-or-verify list.
