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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

