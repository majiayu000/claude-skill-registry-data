---
name: jd-gap-score
description: "Score how well a CV covers a job ad, requirement by requirement, and say honestly what to do about each gap. Use when asked how well do I match this job, score my CV against this job description, what am I missing for this role, or should I apply."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# jd-gap-score

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

Produces a requirement table marked covered, partly covered or missing with the evidence, a fit score with its method shown, and for each gap a truthful framing, a quick way to close it, or advice not to claim it.
