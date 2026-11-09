---
name: context-bankruptcy
description: "Declare bankruptcy on a long-lived AI agent's accumulated memory — audit what it currently believes, separate ground truth from stale and wrong, purge deliberately, restate the truths that survive, and log what was lost. Use when an agent keeps acting on outdated facts, contradicts itself across sessions, 'remembers' things wrong, or after a reorg/pivot makes its worldview obsolete."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# context-bankruptcy

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

Produces a belief audit, a keep/correct/purge ledger, a restated ground-truth file, and the bankruptcy record.
