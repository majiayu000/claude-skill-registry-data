---
name: physio-progress-note
description: "Write a physiotherapy progress note that shows clinical reasoning rather than attendance — what changed against the reassessment markers, what that means for the hypothesis, and what the plan does next. Use when asked to write a progress note, document a follow-up appointment, justify continued treatment to a funder, or when notes read as a list of what was done. A documentation framework for a licensed clinician; the clinical content remains theirs."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# physio-progress-note

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

Produces the reassessment against markers, the interpretation, the plan change with its reason, the objective-measure trend, and the discharge trajectory.
