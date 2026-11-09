---
name: ui-design-pipeline
description: "Run a five-stage UI design pipeline (direction, system, motion, critique, verification) so the result does not look like generic AI output. Use when asked to design or restyle a page, landing page, dashboard or app screen, to make a UI look less AI-generated, or to run the design pipeline. Detects which specialist design skills are installed, hands off to one per stage, and falls back to built-in guidance with the install command when one is missing."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# ui-design-pipeline

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.



## Особенности переноса

- Исходные команды или настройки требуют проверки совместимости.

## Требования к результату

Produces a committed direction, a persisted design system file, a motion spec, a critique with fixes, and browser screenshots at mobile and desktop widths.
