---
name: slo-architect
description: Use when defining, reviewing, or operating SLOs/SLIs/error budgets. Triggers
  on "define an SLO", "what should our SLO be", "error budget", "burn rate", "SLI",
  "service level objective", "Google SRE workbook", "multi-window burn-rate alert",
  or any reliability-target question. Ships SLO designer, error-budget calculator
  with multi-window burn-rate thresholds, and SLO reviewer that catches the common
  bugs (target too aggressive, window too short, conflicting SLOs, no SLI definition).
  4 references on SLO principles + SLI design + error budget math + composition with
  feature-flags-architect/chaos-engineering/kubernetes-operator. NOT a generic observability
  skill — specifically the SLO discipline.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# slo-architect

## Работа в Codex

Прочитай нужные разделы [процедуры](WORKFLOW.md) и только необходимые ресурсы. Пути считай от файла ссылки.
Соблюдай AGENTS.md, цель, стек и полномочия. Навык не разрешает запуск агентов, hooks и фоновых действий.
Используй доступные API Codex и штатный MCP; команды Claude не переноси механически. Укажи недоступные зависимости.
Перед запуском проверь код, зависимости, пути и эффекты. Примеры не доказательство; актуальные API и тарифы сверяй по первоисточникам.
Уточняй существенное; порученные обратимые действия выполняй сам.

