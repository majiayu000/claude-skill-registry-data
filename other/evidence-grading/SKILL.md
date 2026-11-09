---
name: evidence-grading
description: "Grade the evidence behind a claim before betting on it — the hierarchy for business evidence (experiments  usage data  surveys  interviews  anecdotes  opinion), the fit-for-decision test, and the mixed-evidence verdicts that real questions produce. Use when asked how strong is our evidence for this, grade what we know before the decision, is this enough to bet on, or we have three anecdotes and a survey — now what."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# evidence-grading

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

Produces the evidence inventory with grades, the sufficiency verdict against the decision's stakes, and the cheapest-upgrade path.
