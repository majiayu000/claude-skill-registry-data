---
name: report-a-hazard
description: "Report a public hazard or code problem to the authority that can actually fix it — a pothole, broken streetlight, illegal dump, unsafe building, code violation, blocked drain — with the right department, the details that get it actioned, a tracking reference, and an escalation path if it's ignored. Use when someone says 'how do I report a pothole/hazard/violation', 'the council won't fix X', or 'who do I call about Y'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# report-a-hazard

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

Produces a report ready to submit, the right channel, and a follow-up plan.
