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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Локальные assets/ содержат новые автономные примеры и шаблон. Скрипты используют их от корня навыка; примеры не подтверждают работу Anthropic API.
