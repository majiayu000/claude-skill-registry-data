---
name: approval-policy-designer
description: "Design the approval policy for a proactive agent across every connected app: for each kind of action, whether it may act alone, must ask first, or must never do it, with money limits, recipient rules and an audit line. Use when asked what my agent should be allowed to do on its own, set approval rules for Duet, which actions need my yes, design an approval policy for my AI agent, or set spending or sending limits for an agent."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# approval-policy-designer

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

Produces a per-app action table (act, ask, never), the thresholds, the default for anything unlisted, and the one-line rule to paste into the agent's instructions.
