---
name: readonly-mcp-wrapper
description: "Use when asked to expose a folder of notes or docs to Claude or another AI client, build an MCP server over Markdown or JSON files, let an agent read my knowledge base safely, or wrap documentation as MCP tools. To design an MCP server for a whole product, use mcp-server-spec."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# readonly-mcp-wrapper

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

- Исходные команды или настройки требуют проверки совместимости.

## Требования к результату

Produces a read-only MCP server over a folder of Markdown or JSON files: server code using stdio transport, tool definitions, a client configuration snippet, and a safety section confirming no write, delete or network tools are exposed.
