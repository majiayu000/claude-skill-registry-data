---
name: flight-delay-compensation
description: "Work out whether a delayed, cancelled, or overbooked flight likely owes you compensation — and draft the claim with the right rule cited. Use when asked about flight delay compensation, my flight was cancelled/delayed/overbooked, am I owed money for this flight, or how do I claim EU261."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# flight-delay-compensation

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

Produces an eligibility read against the likely-applicable regime (EU261/UK261/US DOT-style and airline duty-of-care), the amount band, the claim letter with flight details, and the evidence to attach — flagging what to verify because rules and thresholds change.
