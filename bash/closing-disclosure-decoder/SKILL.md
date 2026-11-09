---
name: closing-disclosure-decoder
description: "Decode a mortgage Closing Disclosure line by line — which fees are real, which are shoppable or junk, and what changed since the Loan Estimate. Use when asked to decode my closing disclosure, review my closing costs, why did my costs go up, or which fees can I negotiate."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# closing-disclosure-decoder

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

Produces a section-by-section decode, the Loan-Estimate comparison with tolerance flags, the challenge list with scripts, and the cash-to-close verification.
