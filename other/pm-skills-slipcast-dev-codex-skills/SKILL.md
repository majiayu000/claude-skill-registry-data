---
name: pm-skills
description: Use when coordinating project-delivery work across the 8 project-management
  sub-skills — sprint/velocity analytics, portfolio health, Jira/JQL, Confluence,
  Atlassian admin, templates, meeting analysis, team comms. Triggers on 'our sprints
  feel off', 'project health report', 'audit our Jira permissions', 'when will it
  be done', 'run the delivery loop'. Forks context to route to one sub-skill via a
  deterministic signal router and returns a digest; can also drive a full goal→plan→execute→verify→close
  delivery loop through the repo-wide agent-harness with Jira MCP data bridged into
  the domain's analytics tools. Distinct from product-team (what to build vs how to
  deliver it), business-operations (internal ops), and engineering/agent-harness (the
  generic loop engine this orchestrator plugs into).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# pm-skills

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

