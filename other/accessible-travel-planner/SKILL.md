---
name: accessible-travel-planner
description: "Plan a trip that actually works with a disability or access need — confirm real accessibility (not just 'accessible' labels), book the assistance in advance, plan for equipment and medication, and build in the contingencies for when access breaks down. Use when someone says 'plan an accessible trip', 'travelling with a wheelchair/disability', 'book assistance for my flight', or 'will this hotel actually work for me'. Verify specifics with providers."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# accessible-travel-planner

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

Produces an access-verified itinerary, an assistance-booking checklist, an equipment/medication plan, and contingency scripts.
