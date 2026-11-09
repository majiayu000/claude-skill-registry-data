---
name: red-green-proof
description: Turns a suspected bug into a proven one. Verify the cause against reality
  before claiming it, write a test that FAILS on the current code, apply the fix,
  watch it pass — then revert the fix and confirm the test goes red again, because
  a test that passes both ways proves nothing. Invoked bare after a debugging conversation,
  it takes the target from context rather than asking. Use when fixing a bug, investigating
  an incident, hardening a flaky area, or when asked to "add tests that reveal the
  bug". Triggers on "/red-green-proof", "prove the bug", "red-green", "make the test
  fail first", "is that test load-bearing", "reveal the bug with a test".
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# red-green-proof

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

