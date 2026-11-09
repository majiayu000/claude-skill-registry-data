---
name: fleet-maintenance-programme
description: "Design a preventive maintenance programme that keeps vehicles legal and out of the workshop at the wrong moment — intervals set by duty cycle, the inspection items that actually cause roadside failures, and the defect-reporting loop that closes. Use when asked to build a fleet maintenance schedule, set PM intervals, reduce breakdowns or roadside violations, or design a vehicle inspection programme."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# fleet-maintenance-programme

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

Produces the interval schedule by duty cycle, the inspection checklists by level, the defect-reporting and rectification loop, the parts and downtime planning, and the compliance record structure.
