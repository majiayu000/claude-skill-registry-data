---
name: agent-kill-switch-plan
description: "Prepare, before you need it, the runbook for stopping a proactive agent that is misbehaving: how to pause it in seconds, which connections to revoke in what order, how to check what it did, who to tell, and how to restart safely. Use when asked what to do if my agent goes wrong, make a kill switch plan for Duet, how do I stop my AI agent, my agent sent something it should not have, or prepare an emergency plan for an always-on agent."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-kill-switch-plan

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

Produces a one-page runbook with the pause step, the revoke order per connected app, the activity check, message templates for anyone affected, and the restart checklist.
