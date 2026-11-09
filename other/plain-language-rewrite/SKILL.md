---
name: plain-language-rewrite
description: "Rewrite jargon-dense text into plain language without losing precision — the translation pass that keeps every fact and qualifier, the jargon triage (terms to replace, terms to keep-and-define), and the reading-level honesty for the actual audience. Use when asked make this readable, translate this for non-experts, de-jargon this announcement, or rewrite this so my parents/customers/new hires understand it."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# plain-language-rewrite

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

Produces the rewrite with a fidelity check, the jargon ledger, and the kept-terms glossary line.
