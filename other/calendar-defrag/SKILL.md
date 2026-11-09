---
name: calendar-defrag
description: "Defragment a work calendar through a tool-using agent — find the meeting debt, propose the consolidation, and (approval-gated) execute the moves. Use when asked to defrag my calendar, get me focus time, audit my meetings, or fix my week."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# calendar-defrag

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

Produces the calendar audit (cost per meeting, fragmentation map), a defrag proposal with focus blocks, and an approval-gated execution plan.
