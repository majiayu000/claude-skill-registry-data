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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

