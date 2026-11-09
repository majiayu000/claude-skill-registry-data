---
name: dental-recall-reactivation
description: "Build a dental recall and reactivation system that brings lapsed patients back without nagging — the segments worth contacting, the message that works for each, the cadence, and the measure that tells you whether it is working. Use when asked to improve recall rates, reactivate lapsed patients, reduce hygiene no-shows, or fill an empty hygiene column. Communications and operations only; no clinical recall interval is set here."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# dental-recall-reactivation

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

Produces the patient segmentation, per-segment message templates, the contact cadence, the booking-friction fixes, and the metrics to track.
