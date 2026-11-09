---
name: car-lease-decoder
description: "Decode a car lease offer — the money factor converted to APR, the cap-cost math, mileage and disposition traps, and what to negotiate. Use when asked to decode my car lease, is this lease deal good, what's a money factor, or review this lease before I sign."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# car-lease-decoder

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

Produces the real-numbers decode (money factor → APR, total lease cost), the trap list with dollar exposure, and the negotiation points dealers expect to concede.
