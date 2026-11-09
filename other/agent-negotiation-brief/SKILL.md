---
name: agent-negotiation-brief
description: "Brief an AI agent that will negotiate for you with another party's agent or a person (a refund, a price, a meeting time, a contract term): your goal, your opening, your limits, your walk-away point, what it must never reveal, and when it must come back to you. Use when asked to let my agent negotiate, brief my AI for a negotiation, set limits for an agent bargaining on my behalf, or prepare for agent-to-agent negotiation."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-negotiation-brief

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

Produces the brief, the concession ladder, the never-reveal list and the hand-back triggers.
