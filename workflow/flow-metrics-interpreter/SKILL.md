---
name: flow-metrics-interpreter
description: "Read your team's flow metrics — cycle time, throughput, WIP, aging work — and say what they actually mean and what to try, not just restate the numbers. Use when asked to interpret cycle time, what do our flow/Actionable-Agile metrics mean, why is delivery slow, or read our Kanban metrics."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# flow-metrics-interpreter

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

Produces the health read per metric, the likely bottleneck the numbers point to, 2–3 concrete process experiments to run next, and the trap-to-avoid so the team doesn't game the metric instead of fixing the flow.
