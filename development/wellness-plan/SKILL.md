---
name: wellness-plan
description: "Build a preventive-care (wellness) plan for a pet by species, breed, and life stage. Use when asked to create a wellness plan, plan preventive care, set up a vaccination/parasite schedule, or advise an owner on routine care for a puppy/kitten/adult/senior pet."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# wellness-plan

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

Produces a life-stage-appropriate schedule — vaccinations, parasite prevention, dental, nutrition, screening diagnostics, and behavioral guidance — with the rationale, so an owner sees preventive care as a plan, not a series of surprise visits.
