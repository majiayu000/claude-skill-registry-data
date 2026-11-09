---
name: insurance-policy-decoder
description: "Decode a home, renters, or auto insurance policy into what's actually covered, what's excluded, and what the payout math really looks like before you need it. Use when someone asks 'what does my insurance actually cover', 'decode my policy', 'is this deductible normal', or 'actual cash value vs replacement cost'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# insurance-policy-decoder

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

Produces a coverage decode with real payout scenarios, ranked exclusion red flags, the ACV-vs-replacement-cost math, and the questions to ask your agent before renewal.
