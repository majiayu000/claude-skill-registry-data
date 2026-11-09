---
name: regression-test-plan
description: "Design and prioritize a regression test suite so changes don't break what worked. Use when asked to plan regression testing, build a regression suite, decide what to re-test after a change, or trim a bloated regression pack."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# regression-test-plan

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

Produces a risk-based regression plan — what to re-test and why, prioritised tiers (smoke → full), automation candidates, and a run strategy per release — so coverage matches risk and the suite stays fast.
