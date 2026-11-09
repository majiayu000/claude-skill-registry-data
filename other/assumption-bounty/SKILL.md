---
name: assumption-bounty
description: "Extract every hidden assumption from a plan or document and put a price on each one — what it costs if wrong, what it costs to test. Use when about to commit to anything whose author says 'obviously' or whose spreadsheet has hardcoded cells: the bounty hunt makes the invisible load-bearing beliefs explicit and tells you which three to test this week."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# assumption-bounty

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

Produces the assumption ledger (priced and ranked), the cheapest test for each dangerous one, and the document's honest confidence statement.
