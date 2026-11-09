---
name: contract-red-flags
description: "Scan a contract you're about to sign in plain language — surface the clauses that could bite you, what they mean, and what to question or renegotiate. Use when asked to check this contract before I sign, what am I agreeing to, are there red flags in this agreement, or explain this contract's risky bits. Not legal advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# contract-red-flags

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

Produces a plain-English flag list of the risky/unusual clauses (auto-renewal, lock-in, liability, IP, termination, fees), what each means for you, questions to ask, and suggested changes — flagging when it's important enough for a lawyer.
