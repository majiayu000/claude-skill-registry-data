---
name: auto-repair-estimate-decoder
description: "Decode an auto repair estimate — what each line actually is, which items are urgent vs upsell, and the questions that separate a fair shop from a fishing expedition. Use when someone asks 'is this repair quote fair', 'decode my mechanic's estimate', 'do I really need all this', or 'is the shop ripping me off'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# auto-repair-estimate-decoder

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

Produces a line-by-line decode with urgency triage, parts/labor sanity checks, ranked red flags, and the exact questions to ask the shop before authorizing.
