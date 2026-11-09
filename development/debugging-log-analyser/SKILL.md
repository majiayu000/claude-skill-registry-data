---
name: debugging-log-analyser
description: "Parse error logs, stack traces, and crash reports into a structured root cause diagnosis. Use when an application is throwing exceptions, crashing, or producing unexpected errors and you need to understand why and what to fix."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# debugging-log-analyser

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

Produces a structured diagnosis with error classification, stack trace walkthrough, probable root cause with confidence level, affected code path, a concrete code-level fix suggestion, and ordered next debugging steps.
