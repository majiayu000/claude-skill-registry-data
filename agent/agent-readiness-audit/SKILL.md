---
name: agent-readiness-audit
description: "Audit whether AI agents can actually use your product — docs, APIs, onboarding, errors, and discoverability, evaluated from a non-human user's perspective. Use when asked if a product is agent-ready, to audit a site or API for AI usability, to prepare for agentic traffic, or when agents keep failing against your product. For optimising a single article for AI citation use aeo-optimizer; for designing the MCP server itself use mcp-server-spec."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-readiness-audit

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

## Требования к результату

Produces a scored readiness report with per-surface findings and a prioritised fix list.
