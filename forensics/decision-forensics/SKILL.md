---
name: decision-forensics
description: "Reconstruct the decision actually made in a messy Slack, email, or meeting thread into a proper decision record — commitments named, silent assumptions surfaced, non-decisions called out. Use when asked what did we actually decide, turn this thread into a decision record, who committed to what, or reconstruct this discussion."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# decision-forensics

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

Produces a decision record with quoted evidence, a commitments table, reconstructed assumptions, dismissed options, and a confidence note on the reconstruction itself.
