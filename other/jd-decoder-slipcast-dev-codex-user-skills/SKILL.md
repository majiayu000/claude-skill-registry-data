---
name: jd-decoder
description: "Decode a job description to find what they actually want beneath the buzzwords. Use when asked to analyse a job description, decode a JD, assess fit for a role, or figure out what a posting really means before applying."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# jd-decoder

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

Produces a decode — the real must-haves vs. nice-to-haves, hidden priorities & culture signals, red flags, an honest fit assessment, and the exact phrases to mirror in your application.
