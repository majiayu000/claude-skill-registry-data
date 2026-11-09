---
name: cn-quality-traceability
description: "Use when asked 质量追溯体系怎么建, 产品追溯方案, 批次追溯, 一物一码, 客户要求可追溯性, 召回演练, 正向追溯和反向追溯, or plan product and batch traceability in a Chinese factory."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cn-quality-traceability

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

Produces a traceability plan in Chinese: the trace unit and coding rule, the data to capture at each process step (material lots, work orders, equipment, people, inspection results), forward and backward trace paths, record retention, a mock recall drill with a target time, gaps against the current system, and a phased rollout, with industry rules (food, medical devices, automotive) marked to confirm.
