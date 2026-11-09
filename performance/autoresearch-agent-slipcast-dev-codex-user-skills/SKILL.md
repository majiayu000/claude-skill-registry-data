---
name: autoresearch-agent
description: 'Autonomous experiment loop that optimizes any file by a measurable metric.
  Inspired by Karpathy''s autoresearch. The agent edits a target file, runs a fixed
  evaluation, keeps improvements (git commit), discards failures (git reset), and
  loops indefinitely. Use when: user wants to optimize code speed, reduce bundle/image
  size, improve test pass rate, optimize prompts, improve content quality (headlines,
  copy, CTR), or run any measurable improvement loop. Requires: a target file, an
  evaluation command that outputs a metric, and a git repo.'
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# autoresearch-agent

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
