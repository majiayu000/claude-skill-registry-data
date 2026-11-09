---
name: exploratory-test-charter
description: "Write session-based exploratory testing charters to find what scripted tests miss. Use when asked to plan exploratory testing, write a test charter, design a testing session, or do risk-based exploration of a feature."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# exploratory-test-charter

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

Produces focused charters — a mission, areas/risks to explore, tactics and oracles, and timeboxed sessions — so exploration is purposeful and accountable, not random clicking.
