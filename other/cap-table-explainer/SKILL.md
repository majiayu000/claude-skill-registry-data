---
name: cap-table-explainer
description: "Explain a cap table, dilution, SAFEs, option pools, and round mechanics in plain English with the actual math. Use when asked to explain dilution, model a SAFE or priced round, size an option pool, understand a term sheet's economics, or figure out who owns what after a raise. Not legal or financial advice."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# cap-table-explainer

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

Produces a worked ownership breakdown before/after the round, the dilution math step by step, and the traps founders miss.
