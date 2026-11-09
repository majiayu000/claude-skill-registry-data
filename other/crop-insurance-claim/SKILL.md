---
name: crop-insurance-claim
description: "Make a crop or livestock insurance claim after drought, flood, pests, disease or hail: report it in time, record the loss properly, and follow up or appeal if the payout is too low or refused. Use when someone says 'my crop failed, how do I claim', 'the insurance company rejected my crop claim', 'what proof do I need for a crop loss', or 'how do weather-index insurance payouts work'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# crop-insurance-claim

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

Produces a claim timeline, an evidence checklist, a loss record, a notification message, and an appeal plan.
