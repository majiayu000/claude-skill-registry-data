---
name: hire-or-pass
description: "Turn a hiring debrief into a typed decision — hire, hire at a different level, get more signal, or pass — from rubric evidence only, with probabilities and confidence. Use when asked should we hire this candidate, run the debrief, hire or no-hire, or when interviewers disagree and the manager has to call it. Decision support for a human decision — a person owns the hire."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# hire-or-pass

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

Produces the evidence state per competency, the four-way decision with probabilities, the act-or-hold verdict, and when holding, the exact competency to test and who tests it.
