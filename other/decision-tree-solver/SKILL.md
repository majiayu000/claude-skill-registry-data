---
name: decision-tree-solver
description: "Turn a fork-in-the-road decision into a computed expected-value tree — settle or sue, launch or wait, fix or replace — rolled back by the bundled script, with the break-even probability where the answer flips. Use when asked should we settle or go to trial, build a decision tree, what probability makes this worth it, or compare options under uncertainty. Decision support, not advice — the probabilities are yours."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# decision-tree-solver

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

Produces the structured tree, the rollback with the best choice at every fork, the break-even probabilities, and the honest list of what the numbers leave out.
