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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
