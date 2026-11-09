---
name: soap-note
description: "Structure a clinical encounter into a clean SOAP note. Use when asked to write a SOAP note, document a patient encounter, turn visit notes into clinical documentation, or structure subjective/objective/assessment/plan."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# soap-note

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

Produces a well-organised SOAP note — Subjective, Objective, Assessment (with differential), and Plan — from the provided encounter details, in standard clinical-documentation style.
