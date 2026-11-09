---
name: agent-designer
description: 'Use when the user asks to design a multi-agent system, pick an orchestration
  pattern (supervisor/swarm/pipeline), generate tool schemas for agents, or evaluate
  agent execution logs for cost, latency, and failure bottlenecks. Examples: ''design
  an agent architecture for research automation'', ''generate Anthropic tool schemas
  from these tool descriptions'', ''analyze these agent run logs for bottlenecks''.
  NOT for Claude Code workflow files (use workflow-builder) or single-agent prompt
  design (use agent-workflow-designer).'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# agent-designer

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

