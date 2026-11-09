---
name: moving-quote-decoder
description: "Decode a moving-company quote and spot the lowball, the padding, and the outright scam before you book. Use when asked to check a moving quote, is this mover legit, compare moving estimates, or avoid moving scams."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# moving-quote-decoder

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

Produces a read on the quote type (binding vs non-binding vs 'not to exceed') and what it really means, the red flags of moving scams (big deposits, no in-home/video survey, low-then-hostage pricing), the questions to ask and credentials to verify, an apples-to-apples comparison, and how to protect yourself on moving day.
