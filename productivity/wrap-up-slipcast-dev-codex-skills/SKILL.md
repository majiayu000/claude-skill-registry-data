---
name: wrap-up
description: Close out a launched Claude Managed Agent — recap every primitive the
  founder now owns, regenerate the single-file overview page, and suggest the next
  1-2 upgrades. Use when the user says "wrap up", "close this out", "what do I own
  now", "give me the summary", "recap the agent", or when the orchestrator routes
  phase=wrap-up. primitives_inventory.py tables everything owned (agent, environment,
  session, memory, outcome, deployment); overview_page.py regenerates a self-contained
  ./my-agent/agent-overview.html; upgrade_suggester.py ranks the next moves from recorded
  deferrals plus standing hardening steps. Companion to run-without-you; the last
  stop before phase=done.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# wrap-up

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.



## Особенности переноса

- Локальные assets/ содержат новые автономные примеры и шаблон. Скрипты используют их от корня навыка; примеры не подтверждают работу Anthropic API.
