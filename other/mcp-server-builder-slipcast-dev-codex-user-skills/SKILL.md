---
name: mcp-server-builder
description: Design and ship production-ready MCP (Model Context Protocol) servers
  from OpenAPI contracts instead of hand-written tool wrappers. Python and TypeScript
  support, schema validation, safe evolution. Use when exposing an existing API as
  an MCP server, building tool integrations for Claude or Codex or Cursor, or scaffolding
  an MCP project from scratch.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# mcp-server-builder

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

