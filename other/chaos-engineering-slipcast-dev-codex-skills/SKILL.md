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

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

