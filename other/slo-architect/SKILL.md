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

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

