---
name: used-car-decoder
description: "Decode a used-car listing before you drive an hour to see it — what the seller's phrasing is hiding, the history-check items that matter, a test-drive and inspection checklist ordered by cost-of-miss, the questions that make evasive sellers visible, and the walk-away signs ranked 🔴🟡🟢. Use when someone says 'is this car listing legit', 'what should I check on a used car', 'decode this ad', or is about to buy their first car. Not a mechanic — and it says which checks need one."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# used-car-decoder

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

Produces a listing decode, the viewing checklist, and the negotiation frame.
