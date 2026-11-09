---
name: end-of-day-report
description: "Produce an end-of-day report an unattended agent can send honestly: what shipped (verified), what is drafted or waiting, what is blocked and on whom, and tomorrow's first action. Use when asked for an end-of-day report, what did my agent do today, wrap up my day, or a daily close-out summary."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# end-of-day-report

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

Produces a six-line close-out in the shared status vocabulary, every claim cited, with unverified items marked unverified rather than assumed done.
