---
name: chaos-engineering
description: Use when planning, running, or learning from chaos engineering experiments.
  Triggers on "chaos experiment", "fault injection", "gameday", "resilience test",
  "blast radius", "steady state", "abort criteria", "Chaos Toolkit", "Chaos Mesh",
  "Litmus", "Gremlin", "AWS FIS", or any deliberate failure-injection question. Ships
  experiment designer, blast-radius calculator, and postmortem generator (all stdlib
  Python), 4 references on chaos principles + experiment design + attack taxonomy
  + tooling landscape, and a /chaos-experiment slash command. Composes with feature-flags-architect
  (kill switches as abort triggers) and kubernetes-operator (common chaos targets).
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# chaos-engineering

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

