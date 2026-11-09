---
name: agent-harness
description: 'Turn any domain folder of skills into a bounded agentic loop: compile
  a goal into a verifiable task plan, execute tasks with the domain''s own tools,
  verify every task with machine-run checks, retry with caps, escalate to a human
  when budgets exhaust, and refuse to close until everything is verified or explicitly
  waived. Use when you want an agent or subagent to pick up a goal and drive it to
  a verified close across one of this repo''s 20 domains (''run this goal through
  the engineering harness'', ''set up an agentic loop for marketing work'', ''make
  the finance domain self-verifying''). NOT for authoring Claude Code Workflow-tool
  .js scripts (workflow-builder), N-agent tournaments on one task (agenthub), single-file
  metric optimization (autoresearch-agent), or discovering published loop recipes
  (loop-library).'
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# agent-harness

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

