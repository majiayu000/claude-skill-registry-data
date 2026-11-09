---
name: go-bag-builder
description: "Build an emergency go-bag tailored to your actual household and your most likely local hazards — not a generic list — covering the people, pets, medications, documents, and hazard-specific items you'd need to grab and leave in minutes. Use when someone says 'build an emergency kit', 'what goes in a go-bag', 'prepare for evacuation', or 'emergency preparedness for my family'. Points to official preparedness sources for your region."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# go-bag-builder

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

Produces a personalised packing list, a grab-in-2-minutes core, storage and maintenance guidance, and per-person/per-pet additions.
