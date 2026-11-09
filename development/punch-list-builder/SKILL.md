---
name: punch-list-builder
description: "Turn walkthrough notes, photos, or voice-memo transcripts into a proper construction punch list with location, trade, and spec reference per item. Use when asked to build a punch list, clean up walkthrough notes, organise a deficiency list, prep for substantial completion, or track punch items to closeout."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# punch-list-builder

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

Produces a numbered punch list grouped by location with severity tiers, responsible subcontractor, back-charge candidates, and closeout/retainage linkage.
