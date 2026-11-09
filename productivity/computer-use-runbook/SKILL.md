---
name: computer-use-runbook
description: "Write the step-by-step runbook a computer-use or browser agent follows to finish a real online task, such as cancelling a subscription or changing an energy supplier: what to look for on screen, one action per step, how to know it worked, and where to stop for a human. Use when asked to write instructions for a browser agent, make my agent cancel or change something online, or check whether a task is safe to hand to an agent."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# computer-use-runbook

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

Produces the runbook, the stop points and the final verification.
