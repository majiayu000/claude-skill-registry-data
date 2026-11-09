---
name: form-filler-operator
description: "Fill long web forms and applications through a computer-use agent — from a fact sheet you approve, field by field, with a full transcript and nothing submitted without your word. Use when asked to fill this application for me, complete this government/vendor/insurance form, or do this registration."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# form-filler-operator

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

Produces the fact-to-field mapping, the filled form held at review, and a field-level transcript.
