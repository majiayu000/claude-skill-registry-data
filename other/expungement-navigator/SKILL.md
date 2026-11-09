---
name: expungement-navigator
description: "Figure out whether your record can be sealed or expunged, and map the steps to do it — eligibility, waiting periods, forms, and where to get help. Use when asked can I get my record expunged, how do I seal my criminal record, clear my background, or am I eligible for expungement. Not legal advice; expungement law is highly jurisdiction-specific and this points you to the right help."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# expungement-navigator

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

Produces a plain-language read on likely eligibility (offense type, dispositions, waiting periods), the document and step sequence to petition, the costs and fee-waiver options, the realistic timeline, and where to get free or low-cost legal help — so a record that can be cleared actually gets cleared.
