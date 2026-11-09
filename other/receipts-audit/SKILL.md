---
name: receipts-audit
description: "Audit any document against its own sources — every factual claim extracted and graded as evidenced, partially evidenced, unsupported, or contradicted, with the exact source line that supports or fails it. Use when asked to fact-check a document against its sources, check whether a report's claims are backed up, verify a deck against the data, or ask 'does this doc have receipts?'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# receipts-audit

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

Produces a claim ledger, unsupported claims ranked by load-bearingness, a fix-or-drop call per claim, and an honesty score with stated method.
