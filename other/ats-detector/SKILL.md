---
name: ats-detector
description: "Work out which applicant tracking system a job uses from its application link, and give the formatting rules that system parses safely. Use when asked which ATS does this company use, will my CV get through the ATS, is my CV ATS friendly, or how should I format for Workday, Greenhouse, Lever or Taleo."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ats-detector

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

Produces the detected system with the evidence, a parsing-safe formatting checklist, the file type to upload, and a check of a supplied CV against the rules.
