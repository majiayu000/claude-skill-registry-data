---
name: agent-severance
description: "Offboard an AI agent the way you'd offboard an employee — inventory what it knew and touched, export then purge its memory, revoke every credential and access grant, and write the handover for its successor (human or agent). Use when decommissioning an agent or bot, switching agent vendors, ending an AI pilot, or when someone asks 'what did this thing have access to?'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-severance

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

Produces a severance checklist, an access-revocation table, a memory disposition record, and a successor handover.
