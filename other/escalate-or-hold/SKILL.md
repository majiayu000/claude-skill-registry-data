---
name: escalate-or-hold
description: "Decide whether an issue gets escalated now, held with a re-check time, or closed — as a typed decision with probabilities rather than a judgment call in a thread. Use when asked should I escalate this, is this a P1, do we page someone, hold or escalate, or when an on-call, support lead or PM is staring at an issue and unsure."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# escalate-or-hold

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

Produces the issue state in a fixed schema, the three-way decision with probabilities and confidence, the act-or-hold verdict, and the re-check time when holding.
