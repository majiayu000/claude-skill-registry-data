---
name: brief-from-pile
description: "Turn a folder of accumulated documents into one decision-ready brief — the skim-map pass over the pile, the extraction against the brief's actual questions, the conflict reconciliation when documents disagree, and the provenance trail back to sources. Use when asked read all this and tell me what matters, synthesize this folder for the new lead, turn these 20 docs into a brief, or what does all this material actually say."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# brief-from-pile

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

Produces the pile map, the question-driven extraction, the reconciled brief with per-claim sources, and the didn't-read honesty ledger.
