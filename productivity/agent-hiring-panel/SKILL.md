---
name: agent-hiring-panel
description: "Hire an AI agent the way you'd hire an employee — a role spec with success criteria, a structured work-sample interview run on your real tasks, reference checks (what do actual users report), probation KPIs, and termination criteria written before day one. Use when choosing between AI agents/tools/copilots for a job, formalizing an AI pilot, or 'which agent should we use for X'."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-hiring-panel

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

Produces the role spec, interview pack with scoring rubric, a decision record, and a probation plan.
