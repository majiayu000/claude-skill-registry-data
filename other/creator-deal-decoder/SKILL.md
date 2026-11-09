---
name: creator-deal-decoder
description: "Decode a brand deal or UGC contract before signing — usage rights, exclusivity windows, whitelisting, payment terms, and kill clauses ranked 🔴🟡🟢 by what they can cost a creator, plus the counter-ask email. Use when a creator says 'is this brand deal fair', 'what does perpetual usage mean', 'they sent me a contract', or 'should I sign this collab agreement'. Not legal advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# creator-deal-decoder

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

Produces a clause-by-clause decode, a money-math check on the rate, and a ready-to-send negotiation email.
