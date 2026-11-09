---
name: decision-helper
description: "Help me decide between options with a weighted pros/cons that actually reaches a recommendation — not just two lists. Use when asked should I take job A or B, which one should I buy, help me decide, or make a pro/con list."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# decision-helper

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

Produces the criteria that matter (weighted by what you care about), the options scored against them, a clear recommendation with its confidence, and the single question that would flip the decision if you're still torn.
