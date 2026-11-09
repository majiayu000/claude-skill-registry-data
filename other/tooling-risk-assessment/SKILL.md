---
name: tooling-risk-assessment
description: "Assess an injection-mold or production tooling decision before cutting steel — soft vs hard tooling tradeoff, tool life vs forecast, cavitation math, T1 sample timeline, cost of design changes after tooling, and kill criteria. Use when asked whether to kick off tooling, choose soft vs hard tools, size cavities, review a tooling quote, or assess the risk of tooling before the design is frozen."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# tooling-risk-assessment

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

Produces a tooling risk assessment with capacity math, a decision recommendation, and explicit kill criteria.
