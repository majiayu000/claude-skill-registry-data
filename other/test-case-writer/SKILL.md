---
name: test-case-writer
description: "Turn a requirement or user story into clear, executable test cases. Use when asked to write test cases, test scenarios, a test suite for a feature, or to derive tests from acceptance criteria."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# test-case-writer

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

Produces structured test cases — preconditions, steps, test data, expected results — across happy path, edge cases, and negative cases, plus a coverage note, so a tester (or automation) can run them without guessing.
