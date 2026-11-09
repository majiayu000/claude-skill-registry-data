---
name: evt-dvt-pvt-gate-review
description: "Run an NPI phase-gate review for EVT, DVT, or PVT — exit criteria per phase, open-issue triage, yield readout, waiver discipline, and a go/no-go call. Use when asked to run a gate review, decide EVT exit or DVT entry, review build results, assess whether to proceed to the next build, or triage open issues before a phase gate."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# evt-dvt-pvt-gate-review

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

Produces a gate review document with criteria scoring, waiver register, yield analysis, and a defensible go/conditional-go/no-go recommendation.
