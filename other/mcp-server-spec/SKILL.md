---
name: mcp-server-spec
description: "Design an MCP server for a product — the tool surface, auth model, and safety boundaries that make it genuinely usable by AI agents. Use when asked to spec an MCP server, expose a product to agents, design tools for Claude or other MCP clients, or review why an existing MCP server performs badly."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# mcp-server-spec

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

Produces a complete server spec: a small task-shaped toolset with agent-tested descriptions, auth and scoping decisions, error design, and an explicit not-exposed list.
