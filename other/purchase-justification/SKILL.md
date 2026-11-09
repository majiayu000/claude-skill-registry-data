---
name: purchase-justification
description: "Write the purchase request that gets approved — the cost-of-not-buying framing, the ROI math at the approver's altitude, the alternatives-considered section that preempts the obvious pushback, and the right-sized ask for the approval tier. Use when asked justify this tool/hire/equipment purchase, write the budget request, my requests keep getting deferred, or make the business case for this spend."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# purchase-justification

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

Produces the justification memo: the problem priced, the ROI shown, alternatives dispatched, and the ask sized to its approval path.
