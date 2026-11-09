---
name: meetings
description: Use when someone wants to decide whether a meeting is worth calling,
  price a meeting in dollars, build a timeboxed agenda with desired outcomes, or turn
  messy meeting notes into owned action items — or says "should this be a meeting",
  "/cs-meeting-prep", or "/cs-meeting-actions". Runs a cost gate (ASYNC / NOT-READY
  / MEET), builds a decision-first agenda, and extracts an owner + due-date checklist
  that flags every orphan.
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# meetings

## Работа в Codex

Прочитай [предметную процедуру](WORKFLOW.md), затем только нужные разделы ресурсов;
пути разрешай от содержащего их файла. Соблюдай AGENTS.md, цель, стек и полномочия
пользователя. Навык не разрешает создание агентов, hooks или фоновые действия.
Инструменты Claude — обозначения исходной платформы: используй реальные API Codex,
не подменяй CLI механически. Недоступные зависимости укажи; MCP подключай штатно.
До запуска скрипта проверь его код, зависимости, пути и побочные эффекты.
Примеры не подтверждают факты; актуальные API и тарифы проверяй по официальным
источникам. Уточняй существенное, обратимые действия в рамках задачи выполняй сам.

