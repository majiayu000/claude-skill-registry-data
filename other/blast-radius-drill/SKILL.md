---
name: blast-radius-drill
description: "Run the worst-case drill before an agent goes autonomous — the 'if this agent were fully hijacked right now, what's the damage' walk-through, the containment controls (caps, kill-switch, reversibility, isolation), and the recovery plan. Use when asked what's the worst my agent could do, run a blast-radius assessment, prepare for an agent going rogue, or am I ready to let this run unattended."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# blast-radius-drill

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

Produces the worst-case walk-through, the containment controls, the reversibility audit, and the incident-recovery runbook.
