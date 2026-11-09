---
name: health-inspection-prep
description: "Run a self-audit of a food establishment before the health inspector arrives, focused on the violations that actually close kitchens. Use when asked to prep for a health inspection, do a food-safety self-audit, avoid critical violations, or get ready for the health department."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# health-inspection-prep

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

Produces a prioritized checklist organized by risk (critical/priority vs. non-critical), the temperature and hygiene fundamentals, a fix list with owners, and how to handle the inspector on the day.
