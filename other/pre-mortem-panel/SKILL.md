---
name: pre-mortem-panel
description: "Imagine your plan already failed, then get five independent 'here's why it died' stories — before you commit. Use when asked to pre-mortem this, why might this fail, what are the risks before I start, or imagine this went wrong."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# pre-mortem-panel

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

Produces five distinct failure narratives (each from a different cause — execution, timing, people, external, wrong-assumption), the most likely and most lethal among them, the early warning signs of each, and the specific mitigations worth doing now — catching failures while they're still cheap to prevent.
