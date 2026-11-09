---
name: freight-rate-quote
description: "Build a freight rate that covers the cost of actually running the load — the per-mile economics, the deadhead and detention nobody prices, and the accessorials that decide whether the lane is profitable. Use when asked to quote a freight rate, price a lane, work out cost per mile, decide whether to accept a load, or explain why a lane is losing money."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# freight-rate-quote

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

Produces the fully-loaded cost per mile, the lane economics including empty miles, the accessorial schedule, the break-even and target rate, and the accept-or-decline recommendation.
