---
name: data-breach-response
description: "Respond to your data being breached — triage by what actually leaked, the freeze/rotate/monitor ladder in the right order, and the calibrated watchfulness that follows, without panic or paralysis. Use when someone asks my data was in a breach what do I do, I got a breach notification letter, my SSN/ID number leaked, or should I freeze my credit."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# data-breach-response

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

Produces the leaked-data triage, the ordered response ladder with the do-today items, the monitoring plan, and the breach-letter decode (including what the free credit monitoring offer is and isn't).
