---
name: karpathy-coder
description: Use when writing, reviewing, or committing code to enforce Karpathy's
  4 coding principles — surface assumptions before coding, keep it simple, make surgical
  changes, define verifiable goals. Triggers on "review my diff", "check complexity",
  "am I overcomplicating this", "karpathy check", "before I commit", or any code quality
  concern where the LLM might be overcoding.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# karpathy-coder

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.
