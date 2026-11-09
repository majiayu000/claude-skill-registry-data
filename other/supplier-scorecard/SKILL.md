---
name: supplier-scorecard
description: "Build a quarterly supplier performance scorecard with a weighted grade and a clear escalate/develop/exit call. Use when asked to review supplier performance, prepare a quarterly business review for a vendor, score a supplier on OTIF and quality, or decide whether to escalate or exit a supplier."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# supplier-scorecard

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

Produces a weighted scorecard with trend arrows, per-dimension evidence, corrective-action status, and a recommendation.
