---
name: context-switch-recovery
description: "Reconstruct where you were and what's next after an interruption, so a broken focus doesn't cost you the whole thread. Use when asked where was I, I got interrupted and lost my place, help me pick back up, or I forgot what I was doing."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# context-switch-recovery

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

Produces a quick rebuild of the task's state from what you remember (what you'd done, what you were mid-thought on), the single next action to re-enter it, and a 'breadcrumb' habit for next time — cutting the expensive re-immersion cost that interruptions inflict, especially on ADHD brains.
