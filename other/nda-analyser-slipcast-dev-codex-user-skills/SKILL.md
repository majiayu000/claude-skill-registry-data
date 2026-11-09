---
name: nda-analyser
description: "Analyses a Non-Disclosure Agreement clause by clause and flags unusual terms, one-sided provisions, and negotiation points. Use when reviewing an NDA, mutual NDA, confidentiality agreement, or non-disclosure deed before signing or countering."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# nda-analyser

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

Produces a plain English verdict, clause-by-clause risk analysis, and a prioritised negotiation checklist — always with a disclaimer that qualified legal advice is required before signing.
