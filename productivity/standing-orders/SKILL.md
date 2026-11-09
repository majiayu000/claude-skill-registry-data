---
name: standing-orders
description: "Write the operating manual a proactive agent follows between your messages: who is a VIP, what it may always do, what it must never do, the tone it writes in, and when it must stop and ask. Use when asked to write standing orders for my agent, set ground rules for Duet, tell my agent how to behave when I am not there, write my agent's operating manual, or set always and never rules for a proactive agent."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# standing-orders

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

Produces a one-page standing-orders file to paste into the agent's memory or instructions, with the always list, the never list, VIPs, tone rules, escalation triggers and a review date.
