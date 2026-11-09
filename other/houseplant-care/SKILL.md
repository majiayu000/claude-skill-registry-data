---
name: houseplant-care
description: "Diagnose why a houseplant is struggling and set a care routine it'll actually thrive on — matched to your light, home, and how much attention you'll realistically give. Use when asked why is my plant dying, how do I care for a [plant], my plant's leaves are [yellow/brown/drooping], or help me keep this plant alive."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# houseplant-care

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

Produces a likely-cause diagnosis from the symptoms, the specific fix, a simple ongoing care routine (water/light/feed), and honest 'is this the right plant for your space' guidance.
