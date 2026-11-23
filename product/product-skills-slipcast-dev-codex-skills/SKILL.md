---
name: product-skills
description: Use when coordinating product work across the 12 bundled product sub-skills
  (RICE, OKRs, UX research, design tokens, competitive teardown, analytics, experiments,
  discovery, roadmaps, spec-to-repo, landing pages, SaaS scaffolding) or the 4 standalone
  product-team plugins (user stories, Apple HIG, code-to-PRD, research summarizer).
  Triggers on 'help me prioritize', 'plan a product experiment', 'we ship features
  nobody uses', 'run the discovery loop', 'is our OST sound'. Forks context to route
  to one sub-skill via a deterministic signal router and returns a digest; can also
  drive a continuous-discovery loop (Torres cadence tracker + OST linter as machine
  gates) or a full goal→plan→execute→verify→close run through the repo-wide agent-harness.
  Distinct from project-management (how to deliver vs what to build), marketing/landing
  (from-scratch pages), and engineering/agent-harness (the generic loop engine this
  orchestrator plugs into).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# product-skills

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

