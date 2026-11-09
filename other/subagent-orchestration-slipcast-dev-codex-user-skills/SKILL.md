---
name: subagent-orchestration
description: "Decompose work across parallel subagents properly — task slicing that avoids collisions, briefs that stand alone, and result integration that catches contradictions. Use when work can genuinely parallelise (research fan-outs, multi-file changes, independent analyses), when deciding whether to delegate or do it yourself, or when past multi-agent runs produced conflicts and duplicated effort."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# subagent-orchestration

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

Produces an orchestration plan: the parallel/sequential split, per-agent briefs, and the integration protocol.
