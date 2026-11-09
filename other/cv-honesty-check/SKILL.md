---
name: cv-honesty-check
description: "Check a CV for claims that would not survive an interview, a reference or a background check: inflated titles, unprovable numbers, team results claimed as personal, date fudges and skills with no evidence. Use when asked to check my CV is accurate, will my CV hold up in an interview, is this claim too much, or as the last step before sending a CV."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cv-honesty-check

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

Produces a claim-by-claim risk table with the likely interview question, a safer truthful wording for each risky line, and a list of facts to verify before sending.
