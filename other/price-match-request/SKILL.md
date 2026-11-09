---
name: price-match-request
description: "Get a retailer to match a lower price you found — or refund the difference when the price drops right after you bought — with the request written and the exact proof to show. Use when asked for a price match, I found it cheaper somewhere else, the price dropped after I bought it, or can I get a price adjustment."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# price-match-request

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

Produces the policy-aware request, the evidence that qualifies, the eligibility read (what usually counts vs excludes), and a fallback if they won't match.
