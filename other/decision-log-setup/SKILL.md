---
name: decision-log-setup
description: "Set up the team decision log that ends relitigation — the one-line-per-decision format (what, why, who, when, reopening rule), the capture moments wired into existing rituals, and the lookup habit that makes it pay. Use when asked set up a decision log, we keep re-deciding the same things, where do decisions get recorded, or new people keep asking why we do X."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# decision-log-setup

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

Produces the log format, the capture wiring, the reopening rule, and the retrieval habits.
