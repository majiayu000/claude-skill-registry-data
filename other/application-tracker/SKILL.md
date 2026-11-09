---
name: application-tracker
description: "Set up and keep a job application tracker: one master CV, every tailored version, where each was sent, its status, next action and follow-up date, plus a weekly review of what is working. Use when asked to track my job applications, organise my job search, which CV did I send to which company, or what should I follow up on this week."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# application-tracker

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

Produces a tracker table (markdown or CSV) with one row per application, a version log linking each to its tailored CV, this week's actions, and a short weekly review of response rates by source.
